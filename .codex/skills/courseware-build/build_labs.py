#!/usr/bin/env python3
"""
build_labs.py — generate the labs/ folder from labs_data.py (the single source of truth).

For each lab it writes labs/<slug>/lab.md plus the lab's working files (app code,
Dockerfile, docker-compose.yml, Kubernetes YAML), and a labs/README.md index.
Run:  python3 build_labs.py
"""
import os
import shutil
import labs_data as L

ROOT = os.environ.get("COURSE_REPO") or os.getcwd()
LABS_DIR = os.path.join(ROOT, "labs")
APP_DIR = os.path.join(LABS_DIR, "app")


def fence_lang(code):
    head = code.lstrip().split("\n", 1)[0]
    if code.lstrip().startswith("FROM ") or "\nFROM " in code[:40]:
        return "dockerfile"
    if "apiVersion:" in code or head.endswith(":") and ("kind:" in code or "services:" in code):
        return "yaml"
    if code.lstrip().startswith("services:") or "\n  " in code and "image:" in code and "docker " not in code:
        return "yaml"
    return "bash"


def render_md_body(body):
    out = []
    for kind, *rest in body:
        if kind == "h3":
            out.append(f"### {rest[0]}\n")
        elif kind == "p":
            out.append(f"{rest[0]}\n")
        elif kind == "steps":
            out.append("\n".join(f"{i}. {s}" for i, s in enumerate(rest[0], 1)) + "\n")
        elif kind == "code":
            out.append(f"```{fence_lang(rest[0])}\n{rest[0]}\n```\n")
        elif kind == "note":
            out.append(f"> **Note:** {rest[0]}\n")
        elif kind == "table":
            rows = rest[0]
            cells = lambda r: "| " + " | ".join(c.replace("\n", "<br>") for c in r) + " |"
            out.append(cells(rows[0]))
            out.append("| " + " | ".join("---" for _ in rows[0]) + " |")
            for r in rows[1:]:
                out.append(cells(r))
            out.append("")
    return "\n".join(out)


def render_lab_md(lab):
    day = "Day 1 — Docker" if lab["day"] == 1 else "Day 2 — Kubernetes"
    md = []
    md.append(f"# Lab {lab['num']}: {lab['title']}\n")
    md.append(f"> **{day} · {lab['topic']}**  \n> KillerCoda: {lab['killercoda']}\n")
    md.append(f"**Goal:** {lab['goal']}\n")
    md.append(f"**What you'll build:** {lab['build']}\n")
    md.append(render_md_body(lab["body"]))
    md.append(f"> ✅ **Test it:** {lab['test']}\n")
    return "\n".join(md).rstrip() + "\n"


def write_files(folder, manifest):
    for entry in manifest:
        if entry[0] == "write":
            _, rel, content = entry
            dst = os.path.join(folder, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w") as fh:
                fh.write(content)
        elif entry[0] == "copy":
            _, src, rel = entry
            dst = os.path.join(folder, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(APP_DIR, src), dst)


def main():
    for lab in L.LABS:
        folder = os.path.join(LABS_DIR, lab["slug"])
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "lab.md"), "w") as fh:
            fh.write(render_lab_md(lab))
        write_files(folder, lab.get("files", []))

    # labs/README.md index
    lines = ["# Labs — Application Integration with Docker and Kubernetes\n",
             "Hands-on labs for WSQ course **TGS-2021010366**. Every lab builds on the "
             "**TaskBoard** sample app in [`app/`](app/). Work through them in order.\n",
             "## Day 1 — Docker\n",
             "| Lab | Topic | Folder |", "| --- | --- | --- |"]
    for lab in L.DAY1:
        lines.append(f"| {lab['num']} | {lab['topic']} | [{lab['slug']}]({lab['slug']}/) |")
    lines += ["", "## Day 2 — Kubernetes\n", "| Lab | Topic | Folder |", "| --- | --- | --- |"]
    for lab in L.DAY2:
        lines.append(f"| {lab['num']} | {lab['topic']} | [{lab['slug']}]({lab['slug']}/) |")
    lines += ["", "## Assessments\n",
              "Practical assessments are in [`assessments/`](assessments/).\n"]
    with open(os.path.join(LABS_DIR, "README.md"), "w") as fh:
        fh.write("\n".join(lines))

    print(f"Generated {len(L.LABS)} labs into {LABS_DIR}")


if __name__ == "__main__":
    main()
