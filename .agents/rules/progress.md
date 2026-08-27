---
trigger: always_on
description: "Master protocol for documenting progress in tillnow.md and managing files."
---

## Progress Reporting and File Management Protocol

This protocol governs how you document your work in `tillnow.md` and how you manage files and tool outputs. Adhering to this is critical for project tracking and collaboration.

### 1. Read the Implementation Plan First

Before working on any phase, you **MUST** read the `/home/devesh/Hackathon/implementation_plan.md` file to understand:
1.  **Phase requirements:** What tasks must be completed.
2.  **Expected outputs:** What UI screens or backend logic should be created.
3.  **Next phase triggers:** What signals a move to the next phase.

### 2. `tillnow.md` Update Structure

At the conclusion of every significant action or phase, you **MUST** update the `tillnow.md` file. Each phase section must follow this structure:

```markdown
## Phase X: [Phase Name]
**Status:** [COMPLETE | IN PROGRESS | BLOCKED]

**What We Did Now:**
- [Specific task 1] - [Details of what was done.]
- [Specific task 2] - [Details of what was done.]

**Wrong Assumptions Corrected:**
- [Initial Assumption] - [Correction and what was learned.]

**Next Steps:**
- [Detailed plan for the next action.]

**Files Created/Modified:**
- `/path/to/file1` - [Purpose of the file.]
- `/path/to/file2` - [Purpose of the file.]
```

### 3. Blockers Documentation

If you are **BLOCKED**, you must clearly document it in the "Next Steps" section of `tillnow.md`:
1.  **What's blocked:** The specific task you cannot proceed with.
2.  **Why it's blocked:** The missing dependency, tool, API quota, or information.
3.  **What you are waiting for:** The specific input needed from the user.
4.  **Alternative approach:** A potential path forward once unblocked.

### 4. Output Management
Keep track of major CLI outputs (like script errors or LLM benchmark tests). Do not delete past tests unless they clutter the workspace. Save logs or data generations in directories like `/home/devesh/Hackathon/data/`.

### 5. Phase Completion Criteria

A phase is considered **COMPLETE** only when:
- All steps for that phase in `implementation_plan.md` are coded and tested.
- `tillnow.md` is fully updated with the completion status.

---
### **Changelog**
- **2026-03-31:** Adapted tracking logs for the Hackathon AI Ticket Agent Project.
