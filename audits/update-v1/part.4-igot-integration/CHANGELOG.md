# Part 4 — iGOT Karmayogi Integration & Course Recommendation Engine

## Objective
Build the iGOT Karmayogi API integration layer and replace mock course data with real course catalog synchronization.

## 4.1 Create `core/igot_api.py` (NEW FILE)

```python
"""
iGOT Karmayogi API Client — Official integration with iGOT learning platform.
Handles course catalog retrieval, user enrollment tracking, and completion monitoring.
"""
import os
import sys
import json
import time
import asyncio
import requests
from typing import Optional
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class IGOTAPIError(Exception):
    """Custom exception for iGOT API errors."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class IGOTClient:
    """Client for iGOT Karmayogi API integration."""

    def __init__(self):
        self.base_url = settings.igot_api_base_url.rstrip("/")
        self.api_key = settings.igot_api_key
        self.cache_ttl = settings.igot_cache_ttl_seconds
        self._course_cache: Optional[list[dict]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            self._headers["Authorization"] = f"Bearer {self.api_key}"

    def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> dict:
        """Make an authenticated request to iGOT API."""
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.request(
                method, url,
                headers=self._headers,
                timeout=30,
                **kwargs,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            raise IGOTAPIError(
                f"iGOT API {method} {endpoint} failed: {e.response.text}",
                status_code=e.response.status_code,
            )
        except requests.exceptions.Timeout:
            raise IGOTAPIError(f"iGOT API request timed out: {endpoint}")
        except requests.exceptions.ConnectionError:
            raise IGOTAPIError(f"iGOT API connection failed: {endpoint}")

    # ── Course Catalog ──────────────────────────────────────

    def get_course_catalog(self, domain: str = None, page: int = 1, page_size: int = 50) -> list[dict]:
        """
        Retrieve course catalog from iGOT.
        
        Args:
            domain: Filter by domain (e.g., 'technical', 'statistical')
            page: Page number for pagination
            page_size: Results per page (default: 50)
        
        Returns:
            List of course objects with metadata
        """
        # Check cache first
        if (self._course_cache and self._cache_timestamp and
            datetime.now() - self._cache_timestamp < timedelta(seconds=self.cache_ttl)):
            if domain:
                return [c for c in self._course_cache if c.get("domain") == domain]
            return self._course_cache

        try:
            params = {"page": page, "page_size": min(page_size, 100)}
            if domain:
                params["domain"] = domain

            data = self._make_request("/courses", params=params)
            courses = data.get("results", data.get("courses", []))

            # Cache the results
            self._course_cache = courses
            self._cache_timestamp = datetime.now()

            return courses

        except IGOTAPIError:
            # Return cached data even if expired (graceful degradation)
            if self._course_cache:
                print(f"⚠ Using cached iGOT catalog (last sync: {self._cache_timestamp})")
                if domain:
                    return [c for c in self._course_cache if c.get("domain") == domain]
                return self._course_cache
            return []

    def get_course_details(self, course_id: str) -> dict:
        """Get detailed information about a specific course."""
        try:
            data = self._make_request(f"/courses/{course_id}")
            return data
        except IGOTAPIError as e:
            print(f"⚠ Failed to get course details for {course_id}: {e.message}")
            return {}

    def search_courses(self, query: str, domain: str = None) -> list[dict]:
        """
        Search courses by keyword across iGOT catalog.
        
        Uses semantic matching against course titles, descriptions, and skills covered.
        """
        courses = self.get_course_catalog()
        query_lower = query.lower()

        results = []
        for course in courses:
            score = 0
            title = course.get("title", "").lower()
            description = course.get("description", "").lower()
            skills = " ".join(course.get("skills", [])).lower()
            tags = " ".join(course.get("tags", [])).lower()

            if query_lower in title:
                score += 3
            if query_lower in description:
                score += 1
            if query_lower in skills:
                score += 2
            if any(q in tags for q in query_lower.split()):
                score += 1

            if score > 0:
                results.append((score, course))

        # Sort by relevance score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [course for _, course in results[:settings.igot_courses_per_request]]

    # ── User Enrollment ─────────────────────────────────────

    def enroll_user(self, user_id: str, course_id: str) -> dict:
        """
        Enroll a user in a course via iGOT API.
        
        Returns enrollment confirmation or error details.
        """
        try:
            data = self._make_request(
                "/enrollments",
                method="POST",
                json={"user_id": user_id, "course_id": course_id},
            )
            return data
        except IGOTAPIError as e:
            print(f"⚠ Enrollment failed: {e.message}")
            return {"error": e.message, "status": "failed"}

    def get_user_enrollments(self, user_id: str) -> list[dict]:
        """Get all enrollments for a user."""
        try:
            data = self._make_request(f"/users/{user_id}/enrollments")
            return data.get("enrollments", [])
        except IGOTAPIError:
            return []

    def get_course_completion(self, user_id: str, course_id: str) -> dict:
        """Get completion status for a specific course."""
        try:
            data = self._make_request(
                f"/users/{user_id}/courses/{course_id}/completion"
            )
            return data
        except IGOTAPIError:
            return {"enrolled": False, "completed": False, "progress": 0}

    # ── NSSTA TPAC Programme ────────────────────────────────

    def get_tpac_programmes(self) -> list[dict]:
        """
        Get NSSTA Targeted Programme for Capacity Building (TPAC) offerings.
        These are specialized training programmes recommended alongside iGOT courses.
        """
        try:
            # TPAC programmes may be in a separate endpoint or tagged specially
            data = self._make_request("/programs/tpac")
            return data.get("programmes", data.get("programs", []))
        except IGOTAPIError:
            # Fallback: filter iGOT courses by TPAC-relevant tags
            all_courses = self.get_course_catalog()
            tpac_keywords = ["tpac", "capacity building", "statistical", "official", "mospi"]
            tpac_courses = []
            for course in all_courses:
                text = " ".join([
                    course.get("title", ""),
                    course.get("description", ""),
                    " ".join(course.get("tags", [])),
                ]).lower()
                if any(kw in text for kw in tpac_keywords):
                    tpac_courses.append(course)
            return tpac_courses

    # ── Catalog Sync ────────────────────────────────────────

    def sync_catalog(self) -> dict:
        """
        Full catalog synchronization — fetches all courses and stores locally.
        
        Returns sync statistics.
        """
        start_time = time.time()
        total_courses = 0
        domains = set()

        for page in range(1, 11):  # Up to 10 pages
            courses = self.get_course_catalog(page=page)
            if not courses:
                break
            total_courses += len(courses)
            for course in courses:
                domains.add(course.get("domain", "unknown"))

        elapsed = time.time() - start_time

        return {
            "total_courses": total_courses,
            "domains_discovered": list(domains),
            "sync_duration_seconds": round(elapsed, 2),
            "cached": self._cache_timestamp is not None,
            "cache_age_seconds": (
                (datetime.now() - self._cache_timestamp).total_seconds()
                if self._cache_timestamp else None
            ),
        }

    # ── Recommendation Engine ───────────────────────────────

    def recommend_courses_for_gaps(
        self,
        skill_gaps: list[str],
        career_level: str = "intermediate",
        include_tpac: bool = True,
    ) -> dict:
        """
        Generate personalized course recommendations based on skill gaps.
        
        Combines iGOT courses with NSSTA TPAC recommendations.
        
        Returns:
            {
                "recommended_courses": [...],
                "tpac_programmes": [...],
                "learning_pathway": "...",
                "estimated_hours": int,
                "recommended_sequence": [...]
            }
        """
        # Search iGOT courses for each skill gap
        all_recommendations = []
        for gap in skill_gaps:
            courses = self.search_courses(gap)
            for course in courses:
                course["match_score"] = course.get("match_score", 0)
                course["matching_gap"] = gap
                all_recommendations.append(course)

        # Deduplicate by course_id (keep highest match score)
        seen = {}
        for rec in all_recommendations:
            cid = rec.get("id") or rec.get("course_id")
            if cid not in seen or rec.get("match_score", 0) > seen[cid].get("match_score", 0):
                seen[cid] = rec
        deduped = list(seen.values())

        # Sort by match score
        deduped.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        top_courses = deduped[:settings.igot_courses_per_request]

        # Get TPAC programmes
        tpac_programmes = []
        if include_tpac:
            tpac_programmes = self.get_tpac_programmes()

        # Calculate total estimated hours
        total_hours = sum(c.get("duration_hours", 4) for c in top_courses)

        # Build recommended sequence (beginner → advanced)
        recommended_sequence = self._build_learning_sequence(top_courses, skill_gaps)

        return {
            "recommended_courses": top_courses,
            "tpac_programmes": tpac_programmes,
            "total_recommended": len(top_courses),
            "tpac_count": len(tpac_programmes),
            "estimated_hours": total_hours,
            "recommended_sequence": recommended_sequence,
            "skill_gaps_addressed": skill_gaps,
        }

    def _build_learning_sequence(
        self,
        courses: list[dict],
        skill_gaps: list[str],
    ) -> list[dict]:
        """
        Build a logical learning sequence based on difficulty and dependencies.
        Prioritizes courses that address multiple gaps.
        """
        # Simple heuristic: courses with higher match scores first,
        # grouped by domain for coherence
        sequence = []
        for course in courses:
            sequence.append({
                "course_id": course.get("id") or course.get("course_id"),
                "title": course.get("title", course.get("name", "Unknown")),
                "estimated_weeks": max(1, round((course.get("duration_hours", 4) / 4), 0)),
                "difficulty": course.get("difficulty", career_level),
            })
        return sequence
```

## 4.2 Create `core/igot_sync.py` (NEW FILE)

```python
"""
Background synchronization task for iGOT course catalog.
Runs periodically to keep local cache fresh.
"""
import asyncio
import logging
from datetime import datetime

from core.igot_api import IGOTClient, IGOTAPIError

logger = logging.getLogger(__name__)


class IGOTSyncService:
    """Manages periodic synchronization of iGOT catalog."""

    def __init__(self, igot_client: IGOTClient, sync_interval_hours: int = 6):
        self.client = igot_client
        self.sync_interval = sync_interval_hours
        self._task: asyncio.Task | None = None
        self._running = False

    async def start(self):
        """Start background sync loop."""
        self._running = True
        self._task = asyncio.create_task(self._sync_loop())
        logger.info("iGOT sync service started")

    async def stop(self):
        """Stop background sync loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("iGOT sync service stopped")

    async def _sync_loop(self):
        """Periodic sync loop."""
        while self._running:
            try:
                result = await asyncio.to_thread(self.client.sync_catalog)
                logger.info(
                    f"iGOT catalog synced: {result['total_courses']} courses, "
                    f"{result.get('domains_discovered', [])}"
                )
            except IGOTAPIError as e:
                logger.error(f"iGOT sync failed: {e.message}")
            except Exception as e:
                logger.error(f"Unexpected iGOT sync error: {e}")

            await asyncio.sleep(self.sync_interval * 3600)

    async def force_sync(self) -> dict:
        """Trigger immediate catalog sync."""
        return await asyncio.to_thread(self.client.sync_catalog)

    def get_cache_status(self) -> dict:
        """Get current cache status."""
        return {
            "cached": self.client._course_cache is not None,
            "cached_count": len(self.client._course_cache) if self.client._course_cache else 0,
            "cache_timestamp": str(self.client._cache_timestamp) if self.client._cache_timestamp else None,
            "sync_interval_hours": self.sync_interval,
        }
```

## 4.3 Update `core/rag.py` — CourseRecommender

Replace `CourseRecommender` class entirely:

```python
class CourseRecommender:
    """Recommends iGOT courses and NSSTA TPAC programmes for skill gaps."""

    def __init__(self, igot_client: IGOTClient = None):
        self.igot = igot_client or IGOTClient()
        self._local_catalog = None  # Fallback local catalog

    def suggest_courses(
        self,
        skill_gaps: list[str],
        career_level: str = "intermediate",
        include_tpac: bool = True,
    ) -> dict:
        """
        Recommend courses based on skill gaps.
        Falls back to local catalog if iGOT API is unavailable.
        """
        try:
            result = self.igot.recommend_courses_for_gaps(
                skill_gaps, career_level, include_tpac
            )
            return {
                "suggested_pathway": self._generate_pathway_text(result),
                "courses": result["recommended_courses"],
                "tpac_programmes": result.get("tpac_programmes", []),
                "estimated_hours": result["estimated_hours"],
                "recommended_sequence": result["recommended_sequence"],
                "source": "igot_api" if result["total_recommended"] > 0 else "fallback",
            }
        except Exception as e:
            print(f"⚠ iGOT API unavailable, using local catalog: {e}")
            return self._local_recommend(skill_gaps)

    def _generate_pathway_text(self, result: dict) -> str:
        """Generate human-readable learning pathway from recommendations."""
        lines = [
            f"Personalized Learning Pathway for {len(result['skill_gaps_addressed'])} skill gaps:",
            "",
            f"Recommended {result['total_recommended']} courses from iGOT Karmayogi + "
            f"{result.get('tpac_count', 0)} TPAC programmes.",
            f"Estimated total learning time: {result['estimated_hours']} hours.",
            "",
            "Recommended Learning Sequence:",
        ]
        for i, seq in enumerate(result.get("recommended_sequence", []), 1):
            lines.append(
                f"  {i}. {seq['title']} "
                f"({seq.get('estimated_weeks', '?')} weeks, {seq.get('difficulty', '?')} level)"
            )
        return "\n".join(lines)

    def _local_recommend(self, skill_gaps: list[str]) -> dict:
        """Fallback to local course catalog."""
        # Will be populated from local CSV/JSON when iGOT is unavailable
        return {
            "suggested_pathway": "iGOT API unavailable. Please configure IGOT_API_KEY in .env.",
            "courses": [],
            "tpac_programmes": [],
            "estimated_hours": 0,
            "recommended_sequence": [],
            "source": "error",
        }
```

## 4.4 Update `main.py` Lifespan

In `main.py`, add iGOT client initialization:

```python
from core.igot_api import IGOTClient
from core.igot_sync import IGOTSyncService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... existing code ...
    
    # Initialize iGOT client and sync service
    app.state.igot_client = IGOTClient()
    app.state.igot_sync = IGOTSyncService(app.state.igot_client)
    
    # Start background sync
    await app.state.igot_sync.start()
    
    print("  ✓ iGOT Integration Layer loaded")
    
    yield
    
    # Cleanup
    await app.state.igot_sync.stop()
```

## 4.5 Verification Checklist

- [ ] `core/igot_api.py` created with full API client
- [ ] `core/igot_sync.py` created with background sync service
- [ ] `IGOTClient.get_course_catalog()` works with real API
- [ ] `IGOTClient.search_courses()` returns relevant results
- [ ] `IGOTClient.enroll_user()` handles enrollment
- [ ] `IGOTClient.get_tpac_programmes()` returns NSSTA programmes
- [ ] Cache works correctly (30-min TTL)
- [ ] Graceful degradation when API is unavailable
- [ ] `CourseRecommender` uses IGOT client
- [ ] Background sync service starts/stops correctly
- [ ] `main.py` lifespan initializes iGOT components
- [ ] Fallback to local catalog when API fails
