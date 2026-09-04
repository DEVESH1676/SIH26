"""
Comprehensive tests for competency framework (core/competency_framework.py).
Tests framework structure, helper functions, search, and domain access.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCompetencyFrameworkStructure:
    """Test the overall framework structure."""

    def test_framework_has_all_domains(self):
        from core.competency_framework import COMPETENCY_FRAMEWORK
        assert "statistical" in COMPETENCY_FRAMEWORK
        assert "technical" in COMPETENCY_FRAMEWORK
        assert "digital_governance" in COMPETENCY_FRAMEWORK
        assert "behavioural" in COMPETENCY_FRAMEWORK

    def test_statistical_competencies_count(self):
        from core.competency_framework import STATISTICAL_COMPETENCIES
        assert len(STATISTICAL_COMPETENCIES) >= 9

    def test_technical_competencies_count(self):
        from core.competency_framework import TECHNICAL_COMPETENCIES
        assert len(TECHNICAL_COMPETENCIES) >= 10

    def test_digital_governance_competencies_count(self):
        from core.competency_framework import DIGITAL_GOVERNANCE
        assert len(DIGITAL_GOVERNANCE) >= 3

    def test_behavioural_competencies_count(self):
        from core.competency_framework import BEHAVIOURAL_COMPETENCIES
        assert len(BEHAVIOURAL_COMPETENCIES) >= 4

    def test_each_competency_has_required_fields(self):
        from core.competency_framework import COMPETENCY_FRAMEWORK
        for domain, comps in COMPETENCY_FRAMEWORK.items():
            for comp_id, comp in comps.items():
                assert "id" in comp, f"Missing id in {domain}/{comp_id}"
                assert "name" in comp, f"Missing name in {domain}/{comp_id}"
                assert "description" in comp, f"Missing description in {domain}/{comp_id}"
                assert "difficulty_levels" in comp, f"Missing difficulty_levels in {domain}/{comp_id}"

    def test_difficulty_levels_structure(self):
        from core.competency_framework import STATISTICAL_COMPETENCIES
        for comp_id, comp in STATISTICAL_COMPETENCIES.items():
            for level in ["beginner", "intermediate", "advanced"]:
                assert level in comp["difficulty_levels"], f"Missing {level} in {comp_id}"
                assert isinstance(comp["difficulty_levels"][level], list)
                assert len(comp["difficulty_levels"][level]) > 0


class TestGetAllCompetencyIds:
    """Test the get_all_competency_ids helper."""

    def test_returns_ids(self):
        from core.competency_framework import get_all_competency_ids
        ids = get_all_competency_ids()
        assert isinstance(ids, list)
        assert len(ids) > 0

    def test_no_duplicates(self):
        from core.competency_framework import get_all_competency_ids
        ids = get_all_competency_ids()
        assert len(ids) == len(set(ids))

    def test_contains_expected_ids(self):
        from core.competency_framework import get_all_competency_ids
        ids = get_all_competency_ids()
        assert "survey_design" in ids
        assert "python" in ids
        assert "cybersecurity" in ids
        assert "leadership" in ids


class TestGetCompetencyDetails:
    """Test get_competency_details function."""

    def test_existing_competency(self):
        from core.competency_framework import get_competency_details
        details = get_competency_details("survey_design")
        assert details is not None
        assert details["name"] == "Survey Design & Methodology"

    def test_non_existing_competency(self):
        from core.competency_framework import get_competency_details
        details = get_competency_details("nonexistent")
        assert details is None

    def test_competency_id_matches(self):
        from core.competency_framework import get_competency_details
        details = get_competency_details("python")
        assert details["id"] == "TECH-001"

    def test_competency_has_sub_competencies(self):
        from core.competency_framework import get_competency_details
        details = get_competency_details("sampling")
        assert "sub_competencies" in details
        assert len(details["sub_competencies"]) > 0


class TestGetCompetenciesByDomain:
    """Test get_competencies_by_domain function."""

    def test_statistical_domain(self):
        from core.competency_framework import get_competencies_by_domain
        comps = get_competencies_by_domain("statistical")
        assert isinstance(comps, dict)
        assert len(comps) > 0

    def test_nonexistent_domain(self):
        from core.competency_framework import get_competencies_by_domain
        comps = get_competencies_by_domain("nonexistent")
        assert comps == {}

    def test_all_domains_returnable(self):
        from core.competency_framework import get_competencies_by_domain
        for domain in ["statistical", "technical", "digital_governance", "behavioural"]:
            comps = get_competencies_by_domain(domain)
            assert isinstance(comps, dict)


class TestSearchCompetencies:
    """Test search_competencies function."""

    def test_search_by_name(self):
        from core.competency_framework import search_competencies
        results = search_competencies("Python")
        assert len(results) >= 1
        assert any("python" in r["name"].lower() for r in results)

    def test_search_case_insensitive(self):
        from core.competency_framework import search_competencies
        results_upper = search_competencies("SURVEY")
        results_lower = search_competencies("survey")
        assert len(results_upper) == len(results_lower)

    def test_search_by_description(self):
        from core.competency_framework import search_competencies
        results = search_competencies("sampling")
        assert len(results) >= 1

    def test_search_by_sub_competency(self):
        from core.competency_framework import search_competencies
        results = search_competencies("probability sampling")
        assert len(results) >= 1

    def test_search_no_results(self):
        from core.competency_framework import search_competencies
        results = search_competencies("zzzznotfound")
        assert results == []

    def test_search_returns_expected_fields(self):
        from core.competency_framework import search_competencies
        results = search_competencies("Python")
        for result in results:
            for key in ["id", "name", "domain", "description"]:
                assert key in result, f"Missing {key} in search result"


class TestSpecificCompetencies:
    """Test specific competency definitions."""

    def test_survey_design(self):
        from core.competency_framework import STATISTICAL_COMPETENCIES
        comp = STATISTICAL_COMPETENCIES["survey_design"]
        assert comp["id"] == "STAT-001"
        assert len(comp["sub_competencies"]) == 5
        assert len(comp["difficulty_levels"]["beginner"]) >= 1

    def test_python(self):
        from core.competency_framework import TECHNICAL_COMPETENCIES
        comp = TECHNICAL_COMPETENCIES["python"]
        assert comp["id"] == "TECH-001"
        assert "Python fundamentals" in comp["sub_competencies"]
        assert "Python syntax and data types" in comp["difficulty_levels"]["beginner"]

    def test_sql(self):
        from core.competency_framework import TECHNICAL_COMPETENCIES
        comp = TECHNICAL_COMPETENCIES["sql"]
        assert comp["id"] == "TECH-003"
        assert len(comp["sub_competencies"]) == 4

    def test_cybersecurity(self):
        from core.competency_framework import DIGITAL_GOVERNANCE
        comp = DIGITAL_GOVERNANCE["cybersecurity"]
        assert comp["id"] == "DG-001"
        assert "Security awareness" in comp["sub_competencies"]

    def test_ethics(self):
        from core.competency_framework import BEHAVIOURAL_COMPETENCIES
        comp = BEHAVIOURAL_COMPETENCIES["ethics"]
        assert comp["id"] == "BEH-004"
        assert "Fundamental principles of official statistics" in comp["sub_competencies"]
