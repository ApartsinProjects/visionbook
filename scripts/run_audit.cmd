@echo off
rem VisionBook QA gate: runs the book-skills audit-plugin pipeline (150 checks, P0-P3)
rem against this book. Same pipeline as the LLMBook. Usage:
rem   scripts\run_audit.cmd                 (all checks)
rem   scripts\run_audit.cmd --priority P0   (KDP/Kindle blockers only)
rem   scripts\run_audit.cmd --list          (list available checks)
rem Note: OFFTOPIC_NO_LLM_CONTEXT is LLMBook-specific; ignore its findings here.
cd /d E:\Projects\claude-skills\book-skills
C:\Python314\python.exe -m scripts.audit.run --root E:\Projects\VisionBook %*
