# Nobody Assigned This

A two-week course in agency for a 15-year-old who's already good at homework: 8 sessions (230 guided minutes), real-world challenges between sessions, a capstone with a real outside user, a reflection journal, two quizzes, and a parent/mentor guide.

## Start here

- **Web version:** `nobody-assigned-this.html` (one self-contained page; open it in a browser)
- **Everything in one file:** `Nobody_Assigned_This_FULL_COURSE.md`
- **Read first:** `00_README_Assumptions_and_Packaging.md`

## Files

| File | For |
|---|---|
| `01_Course_Overview_and_Schedule.md` | Student + parent (print as the one-page schedule) |
| `02_Student_Workbook_Sessions.md` | Student: Sessions 1–8 |
| `03_Capstone_Project.md` | Student + parent: ideas, brief template, demo format, rubric |
| `04_Reflection_Journal.md` | Student: self-ratings, prompts, logs |
| `05_Quizzes_Student.md` | Student: printable quiz sheets |
| `06_Quiz_Answer_Keys_PARENT.md` | Parent only |
| `07_Parent_Mentor_Guide.md` | Parent / mentor |

## Rebuilding the web page

The HTML is generated from the Markdown files:

```bash
python3 -m venv .venv && .venv/bin/pip install markdown
.venv/bin/python build/build_page.py
```

Quotes are attributed to their authors as originally posted.
