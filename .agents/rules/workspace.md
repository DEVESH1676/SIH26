---
trigger: always_on
description: "Master protocol for workspace interaction, including file, folder, and command verification."
---

## Collaborative Workspace and Execution Protocol

To ensure seamless collaboration and prevent errors, you must treat the workspace as a dynamic environment and verify all actions before execution.

### 1. Collaborative Workspace Awareness (The "Why")

This project is worked on by **multiple agents concurrently**. The file structure can change between sessions without your knowledge. Never assume anything exists—always verify. Failing to do so can lead to working with outdated information, overwriting another agent's work, or executing invalid commands.

### 2. File and Folder Verification (The "How")

Before ANY file operation (read, write, edit, delete), you **MUST** verify the state of the filesystem.

*   **Check Directory Contents:**
    ```bash
    # Get a quick overview of a directory
    ls -la /path/to/dir/
    ```

*   **Verify Existence Before Acting:**
    ```bash
    # Check if a directory exists
    test -d /path/to/dir && echo "EXISTS" || echo "MISSING"
    # Check if a file exists
    test -f /path/to/file && echo "EXISTS" || echo "MISSING"
    ```

*   **Project Path Conventions:**
    *   Project Root: `/home/devesh/Hackathon/`
    *   Python Virtual Env: `/home/devesh/Hackathon/venv/`
    *   Core Logic: `/home/devesh/Hackathon/core/`
    *   Dataset Storage: `/home/devesh/Hackathon/data/`
    *   Vector DB: `/home/devesh/Hackathon/chroma_db/`

### 3. Python Execution Protocol

Before running python files, you **MUST** activate the virtual environment:
```bash
source venv/bin/activate && python script.py
```

### 4. Error Handling

If a file or directory is missing when it should exist:
1.  Document the missing path in `tillnow.md`.
2.  Note the impact on the current execution.
3.  Suggest recovery steps or request user intervention.

---
### **Changelog**
- **2026-03-31:** Updated environment paths to the Hackathon structure (venv, core, data, chroma_db).

---
**Acknowledgment:** okay from now on keep that in mind
