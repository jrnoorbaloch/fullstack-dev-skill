---
description: Find the root cause of a bug or error and fix it
argument-hint: "<error message or what is going wrong>"
---
Use the fullstack-wordpress skill to fix this problem: $ARGUMENTS

1. Read the relevant code and reproduce the problem (run it, or write a failing test).
2. Find the root cause — explain it in 1–3 sentences.
3. Make the smallest correct fix, matching the project's style.
4. Re-run the reproduction and `scripts/verify.py`; add a regression test where practical.
5. Summarise what was wrong and what changed.
