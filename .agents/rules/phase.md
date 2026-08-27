---
trigger: always_on
---

# Phase-Driven Development Protocol

## Work in Phases - No Skipping

Work **strictly** in phases as defined in `implementation_plan.md`:

```
Phase 1: Data & Setup
  └─ 1.1: Environment configuration
  └─ 1.2: Synthetic data generation
  └─ 1.3: Vector database ingestion

Phase 2: Classification Core
  └─ 2.1: Establish category centroids
  └─ 2.2: Build similarity matcher
  └─ 2.3: Test classification accuracy

Phase 3: RAG & Resolution
  └─ 3.1: Build semantic retrieval mechanism
  └─ 3.2: Implement LLM resolution generation

Phase 4: Agentic Layer & UI
  └─ 4.1: Escalation logic rules
  └─ 4.2: Repeat detection (automation playbook suggestion)
  └─ 4.3: Streamlit dashboard implementation
```

## Phase Completion Checklist

Before marking a phase COMPLETE:
- [ ] All required code for the phase in `implementation_plan.md` is functioning and tested.
- [ ] `tillnow.md` is updated with completion status.
- [ ] Next phase steps are noted.

## Blockers Protocol

If blocked (e.g., LLM timeouts, missing dependencies):
1. Document in `tillnow.md` under "Next Steps".
2. List what the user needs to provide or decide on.
3. Note an alternative approach (e.g., fallback scripts) for once unblocked.

## Never Skip Documentation

Even failed attempts must be documented in `tillnow.md`:
- What was attempted
- Why it failed
- What to try next

**"No documentation = no progress tracking = phase never completes."**

---
### **Changelog**
- **2026-03-31:** Adapted from Pentest protocol to AI Ticket Agent Hackathon development structure.
- **2026-04-08:** Added Autonomous GSD Pipeline Execution rule.

## Autonomous GSD Pipeline Execution (The "Do Phase X" Rule)
When the user explicitly says **"do phase [N]"** (e.g., "do phase 1", "do phase 2"), you MUST NOT ask for further step-by-step permission to run the phase. Instead, you MUST autonomously string together the entire GSD pipeline for that phase from start to finish, and deliver a final report.

The required execution chain for "do phase [N]" is:
1. **Discuss:** Run `[/gsd-discuss-phase [N]]` (using the `--chain` and `--batch` concepts if applicable) to finalize phase context.
2. **Plan:** Run `[/gsd-plan-phase [N]]` to generate the XML task plans based on the discussion outputs.
3. **Execute:** Run `[/gsd-execute-phase [N]]` to execute the wave-based tasks and write the actual code.
4. **Verify:** Run `[/gsd-verify-work [N]]` to extract deliverables, run the UAT tests automatically or interactively, diagnose failures, and apply fixes until all tests pass.
5. **Ship (if applicable):** Run `[/gsd-ship [N]]` to create a PR or finalize the work branch.
6. **Report:** Generate a comprehensive markdown report to the user summarizing:
   - What was discussed and planned.
   - What was executed (files created/modified).
   - Verification results (UAT outcomes and fix loops).
   - "Ready for next phase" status.

During this autonomous loop, you are authorized to read the resulting `CONTEXT.md`, `PLAN.md`, `SUMMARY.md`, and `UAT.md` files yourself and take the next required action in the chain without stalling for user prompts, unless an unresolvable blocker or subjective design decision explicitly stops the workflow.
