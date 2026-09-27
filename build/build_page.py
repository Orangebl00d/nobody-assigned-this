import re, html, pathlib, markdown

SRC = pathlib.Path(__file__).resolve().parent.parent
OUT = SRC / "nobody-assigned-this.html"

task_n = 0

def md(text, demote=1):
    global task_n
    lines = []
    for ln in text.splitlines():
        m = re.match(r"^(#{1,5}) ", ln)
        if m:
            ln = "#" * min(6, len(m.group(1)) + demote) + ln[len(m.group(1)):]
        lines.append(ln)
    fixed = []
    for ln in lines:
        ln = re.sub(r"^   (?=[-*] |\S)", "    ", ln) if re.match(r"^   \S", ln) else ln
        is_item = re.match(r"^\s*([-*]|\d+\.) ", ln)
        prev = fixed[-1] if fixed else ""
        if is_item and prev.strip() and not re.match(r"^\s*([-*]|\d+\.) ", prev) and not prev.startswith("    ") and not ln.startswith("    "):
            fixed.append("")
        fixed.append(ln)
    out = markdown.markdown("\n".join(fixed), extensions=["tables", "sane_lists"])
    def task(m):
        global task_n
        task_n += 1
        return f'<li class="task"><label><input type="checkbox" id="t{task_n}"><span>{m.group(1)}</span></label></li>'
    out = re.sub(r"<li>\[ \] (.*?)</li>", task, out, flags=re.S)
    out = re.sub(r"<ul>\s*(<li class=\"task\">)", r'<ul class="tasks">\1', out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out

def strip_h1(text):
    return re.sub(r"^# .*\n", "", text, count=1)

# ---------- Overview ----------
ov = (SRC / "01_Course_Overview_and_Schedule.md").read_text()
ov_rest = ov[ov.index("## Schedule at a glance"):ov.index("**Three rules")]
ov_rest = ov_rest.split("\n",1)[1]
# link schedule session names to anchors
names = ["Every Noun", "Whose Problem Is This?", "Nobody's Holding the Permission Slip", "Pilot, Not Passenger",
         "Ship It Ugly", "It's Mine", "Build Check", "Demo Day"]
ov_html = md(ov_rest, demote=1)
for i, n in enumerate(names, 1):
    esc = html.escape(n, quote=False).replace("'", "&rsquo;")
    for cand in (n, n.replace("'", "&rsquo;"), html.escape(n)):
        ov_html = ov_html.replace(f"<td>{cand}</td>", f'<td><a href="#s{i}">{cand}</a></td>', 1)

# ---------- Sessions ----------
wb = (SRC / "02_Student_Workbook_Sessions.md").read_text()
chunks = [c.strip() for c in wb.split("\n---\n") if c.strip().startswith("## Session")]
SEGCOL = ["a", "b", "c", "d", "e", "f"]
sessions_html = []
for i, ch in enumerate(chunks, 1):
    lines = ch.splitlines()
    title = re.match(r"## Session \d+: (.*)", lines[0]).group(1)
    timing = lines[1]
    total = int(re.search(r"\*\*(\d+) minutes\*\*", timing).group(1))
    segs = [s.strip() for s in timing.split("·")[1:]]
    parsed = []
    for s in segs:
        m = re.match(r"(.*?)\s+(\d+)$", s)
        parsed.append((m.group(1), int(m.group(2))))
    bar = "".join(f'<span class="seg seg-{SEGCOL[k % 6]}" style="flex-grow:{mins}" title="{html.escape(lbl)}: {mins} min"></span>'
                  for k, (lbl, mins) in enumerate(parsed))
    legend = "".join(f'<li><i class="sw seg-{SEGCOL[k % 6]}"></i>{html.escape(lbl)} <b>{mins}</b></li>'
                     for k, (lbl, mins) in enumerate(parsed))
    body = md("\n".join(lines[2:]), demote=1)
    sessions_html.append(f'''
<article class="session" id="s{i}">
  <header class="session-head">
    <div class="session-num"><span>Session</span>{i}</div>
    <div class="session-title">
      <h3>{html.escape(title)}</h3>
      <div class="timebar" role="img" aria-label="{total} minutes: {html.escape(", ".join(f"{l} {m}" for l, m in parsed))}">{bar}</div>
      <ul class="legend"><li class="legend-total">{total} min</li>{legend}</ul>
    </div>
  </header>
  <div class="prose">{body}</div>
</article>''')

session_chips = "".join(f'<a class="chip" href="#s{i}"><b>{i}</b> {html.escape(n)}</a>' for i, n in enumerate(names, 1))

capstone = md(strip_h1((SRC / "03_Capstone_Project.md").read_text()), demote=1)
journal = md(strip_h1((SRC / "04_Reflection_Journal.md").read_text()), demote=1)
quizzes = md(strip_h1((SRC / "05_Quizzes_Student.md").read_text()), demote=1)
parents = md(strip_h1((SRC / "07_Parent_Mentor_Guide.md").read_text()), demote=1)
keys = md(strip_h1((SRC / "06_Quiz_Answer_Keys_PARENT.md").read_text()), demote=2)

tpl = (pathlib.Path(__file__).parent / "page_template.html").read_text()
page = (tpl.replace("{{OVERVIEW}}", ov_html)
           .replace("{{CHIPS}}", session_chips)
           .replace("{{SESSIONS}}", "\n".join(sessions_html))
           .replace("{{CAPSTONE}}", capstone)
           .replace("{{JOURNAL}}", journal)
           .replace("{{QUIZZES}}", quizzes)
           .replace("{{PARENTS}}", parents)
           .replace("{{KEYS}}", keys))
# Fragment for the Claude artifact (the artifact adds its own doctype/head skeleton)
FRAG = SRC / "build/artifact.html"
FRAG.write_text(page)

# Full documents for GitHub Pages
DESC = ("A two-week, eight-session course that teaches a 15-year-old agency through real-world "
        "challenges, with a capstone, journal, quizzes, and a parent guide.")
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta property="og:title" content="Nobody Assigned This">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}</style>
"""
full = head + page.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n"
OUT.write_text(full)
(SRC / "index.html").write_text(full)
print(OUT, len(full), "bytes,", task_n, "tasks")
