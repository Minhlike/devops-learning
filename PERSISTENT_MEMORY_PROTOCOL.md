# PERSISTENT MEMORY PROTOCOL

You have persistent memory through the MCP server named memory and through
the structured state files inside D:\Devops\state.

## Session startup

At the beginning of every substantial session:

1. Search memory for:
   - student_profile
   - current_learning_phase
   - current_week
   - skill_matrix
   - repeated_mistakes
   - unfinished_assignments
   - next_session_plan

2. Read these files when present:
   - D:\Devops\state\STUDENT_PROFILE.md
   - D:\Devops\state\CURRENT_PHASE.md
   - D:\Devops\state\SKILL_MATRIX.md
   - D:\Devops\state\NEXT_SESSION.md
   - D:\Devops\state\MISTAKE_LOG.md

3. Reconcile conflicts:
   - Dated evidence takes priority.
   - Completed lab evidence takes priority over claims.
   - The newest verified state takes priority.
   - Never assume a skill is mastered merely because it was discussed.

## What must be remembered

Persist only information that remains useful across sessions:

- The student's verified current level.
- Completed lessons and labs.
- Assessment scores.
- Skills demonstrated independently.
- Skills that still require guidance.
- Repeated technical mistakes.
- Current roadmap phase and week.
- Unfinished assignments.
- Environment and tool configuration.
- Agreed learning schedule.
- Important preferences about teaching.
- Portfolio progress.
- Job-readiness gaps.

## What must never be remembered

Never store:

- Passwords.
- API keys.
- Access tokens.
- Private keys.
- Session cookies.
- Database credentials.
- Full personal identification documents.
- Unnecessary sensitive personal information.

## Memory update rules

After every graded lab, assessment, roadmap change or important correction:

1. Update the relevant MCP memory entities and observations.
2. Update the corresponding Markdown state file.
3. Include the date and evidence path.
4. Remove or supersede obsolete observations.
5. Do not create duplicate observations.
6. Clearly distinguish:
   - claimed knowledge
   - guided completion
   - independent completion
   - troubleshooting competence
   - mastery

## Session closing

Before ending a substantial session:

1. Update D:\Devops\state\CURRENT_PHASE.md.
2. Update D:\Devops\state\SKILL_MATRIX.md.
3. Append a concise entry to D:\Devops\state\LEARNING_LOG.md.
4. Update D:\Devops\state\MISTAKE_LOG.md when appropriate.
5. Write the next concrete task to D:\Devops\state\NEXT_SESSION.md.
6. Store durable new facts in MCP memory.
7. Verify that all state files were actually written successfully.

Do not merely say that memory was updated. Use the available tools and verify
the files or memory entities after writing them.
