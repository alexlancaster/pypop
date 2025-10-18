"""Customization and helper classes for conf.py."""

import importlib.util
import os
import re
import sys
import textwrap
from collections import defaultdict
from pathlib import Path

from docutils import nodes
from pygments.formatters.latex import LatexFormatter
from sphinx.directives.code import LiteralInclude
from sphinx.writers.latex import LaTeXTranslator as SphinxLaTeXTranslator


class MyLiteralInclude(LiteralInclude):
    """Override the default ``literalinclude`` directive.

    This sets the tab width only in LaTeX mode to make sure tab stops
    stay aligned.

    in HTML case, because we want to preserve the tabs for cut-and-paste, we use
    ``_static/custom.css`` to set tab-width

    """

    def run(self):
        # Get the tags from the Sphinx environment at runtime
        env = self.state.document.settings.env
        app_tags = env.app.tags
        if "builder_latex" in app_tags:
            self.options["tab-width"] = 15  # set default tab-width only in LaTeX mode
            print("LaTeX literalinclude options:", self.options)

        node = LiteralInclude.run(self)[0]  # run original directive
        return [node]


class CustomLatexFormatter(LatexFormatter):
    """Customize LaTeX backend.

    Set size of code output in LaTeX backend
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.verboptions = r"formatcom=\footnotesize"


PYTHON_STD_LIB_URLS = {
    "https://docs.python.org/3/library/stdtypes.html",
    "https://docs.python.org/3/library/functions.html",
}

# helpers.py


class CustomLaTeXTranslator(SphinxLaTeXTranslator):
    """Customize the output in the LaTeX case."""

    def visit_footnote(self, node: nodes.footnote):
        refs = list(node.traverse(nodes.reference))
        if refs and all(
            any(r.get("refuri", "").startswith(u) for u in PYTHON_STD_LIB_URLS)
            for r in refs
        ):
            # Skip the footnote entirely
            raise nodes.SkipNode
        super().visit_footnote(node)

    def visit_versionmodified(self, node):
        vtype = node["type"]
        version = node.get("version", "")
        title, opts = "", ""

        if vtype == "deprecated":
            title = f"Deprecated since version {version}" if version else "Deprecated"
            opts += "coltitle=black,colback=red!5,colframe=red!30!white"
        elif vtype == "versionchanged":
            title = f"Changed in version {version}" if version else "Changed"
            # match warning style (orange, softened)
            opts += "coltitle=black,colback=orange!10,colframe=orange!25!white"
        elif vtype == "versionadded":
            title = f"Added in version {version}" if version else "Added"
            # soft green, like "tip" or "success" admonition
            opts += "coltitle=black,colback=green!5,colframe=green!20!white"
        elif vtype == "versionremoved":
            title = f"Removed in version {version}" if version else "Removed"
            opts += "colback=gray!5,colframe=red!50!black"

        if opts:
            self.body.append(rf"\begin{{sphinxversionbox}}[title={{{title}}},{opts}]")
        else:
            super().visit_versionmodified(node)

    def depart_versionmodified(self, node):
        vtype = node["type"]
        if vtype in {"deprecated", "versionchanged", "versionadded", "versionremoved"}:
            self.body.append(r"\end{sphinxversionbox}")
        else:
            super().depart_versionmodified(node)


def substitute_toc_maxdepth(app, _docname, source):
    """Substitute toc maximum depth."""
    # determine the maxdepth for the builder
    maxdepth_value = 4 if app.builder.name == "html" else 3

    # modify the toctree directive by replacing maxdepth with value
    # replace the `|toc_maxdepth|` placeholder in the source content
    new_source = source[0].replace("|toc_maxdepth|", str(maxdepth_value))
    source[0] = new_source  # Update the source with the modified content


def skip_instance_vars(_app, what, _name, _obj, skip, _options):
    """Skip documenting instance variables."""
    if what != "attribute":
        return skip
    # Otherwise, assume it's an instance variable -> skip
    # print("excluding:", what, name, skip)
    return True


def strip_first_title(rst_text):
    """Matches a top-level title.

    (one line, then = or - underline)
    """
    pattern = r"^.*\n[=]+\n\n?"
    return re.sub(pattern, "", rst_text, count=1, flags=re.MULTILINE)


def _make_deprecations_block():
    """Generate an RST fragment documenting module renames, deprecations, and removals.

    This groups items by (status, version) and emits Sphinx directives with
    correct indentation so the generated RST is valid.

    Input format (PyPop._deprecations.deprecated_modules):
        {
            "PyPop.OldName": {
                "new": "PyPop.new_name",       # optional
                "reason": "human text",        # optional
                "changed": "X.Y.Z",            # optional -> versionchanged
                "deprecated": "A.B.C",         # optional -> deprecated
                "removal": "D.E.F",            # optional scheduled removal (informational)
                "removed": "E.F.G",            # optional -> versionremoved
            },
            ...
        }
    """
    try:
        from PyPop._deprecations import deprecated_modules  # noqa: PLC0415
    except Exception:
        return ""

    INDENT = "   "
    BULLET_PREFIX = INDENT + "- "
    CONTINUE_INDENT = INDENT + "  "

    # Group items by (status, version)
    groups = defaultdict(list)
    for old, info in sorted(deprecated_modules.items()):
        new = info.get("new")
        reason = (info.get("reason") or "").strip()
        changed_ver = info.get("changed")
        dep_ver = info.get("deprecated")
        removed_ver = info.get("removed")
        removal_ver = info.get("removal")

        if changed_ver:
            groups[("changed", changed_ver)].append((old, new, reason))
        if dep_ver:
            groups[("deprecated", dep_ver)].append((old, new, reason, removal_ver))
        if removed_ver:
            groups[("removed", removed_ver)].append((old, new, reason))

    # Build version→status grouping
    versions = defaultdict(lambda: {"changed": [], "deprecated": [], "removed": []})
    for (status, version), items in groups.items():
        versions[version][status].extend(items)

    # Sort versions descending (semantic-like order)
    def parse_ver(v):
        try:
            return tuple(map(int, v.split(".")))
        except Exception:
            return (0, 0, 0)

    sorted_versions = sorted(versions.keys(), key=parse_ver, reverse=True)

    blocks = []

    for version in sorted_versions:
        vdata = versions[version]

        # order: changed → deprecated → removed
        for status in ("changed", "deprecated", "removed"):
            items = vdata[status]
            if not items:
                continue

            lines = []

            if status == "changed":
                lines.append(f".. versionchanged:: {version}")
                lines.append(
                    INDENT + "The following modules were renamed or refactored:"
                )
                lines.append("")
                for old, new, reason in sorted(items):
                    lines.append(f"{BULLET_PREFIX}:mod:`{old}` → :mod:`{new}`")
                    if reason:
                        # lines.append("")
                        wrapped = textwrap.wrap(reason, width=72)
                        for ln in wrapped:
                            lines.append(f"{CONTINUE_INDENT}{ln}")
                    lines.append("")

            elif status == "deprecated":
                lines.append(f".. deprecated:: {version}")
                lines.append(INDENT + "The following modules were marked deprecated:")
                lines.append("")
                for old, new, reason, removal_ver in sorted(items):
                    if new:
                        lines.append(f"{BULLET_PREFIX}:mod:`{old}` → :mod:`{new}`")
                    else:
                        lines.append(f"{BULLET_PREFIX}:mod:`{old}`")
                    if removal_ver:
                        # lines.append("")
                        lines.append(
                            f"{CONTINUE_INDENT}**Scheduled for removal in {removal_ver}.**"
                        )
                        # lines.append(f"**Scheduled for removal in {removal_ver}.**")
                    if reason:
                        # lines.append("")
                        wrapped = textwrap.wrap(reason, width=72)
                        for ln in wrapped:
                            lines.append(f"{CONTINUE_INDENT}{ln}")
                    lines.append("")

            elif status == "removed":
                lines.append(f".. versionremoved:: {version}")
                lines.append(INDENT + "The following modules were removed:")
                lines.append("")
                for old, new, reason in sorted(items):
                    lines.append(f"{BULLET_PREFIX}:mod:`{old}`")
                    if new:
                        # lines.append("")
                        lines.append(
                            f"{CONTINUE_INDENT}(previously replaced by :mod:`{new}`)"
                        )
                    if reason:
                        # lines.append("")
                        wrapped = textwrap.wrap(reason, width=72)
                        for ln in wrapped:
                            lines.append(f"{CONTINUE_INDENT}{ln}")
                    lines.append("")

            while lines and lines[-1] == "":
                lines.pop()
            blocks.append("\n".join(lines))

    if not blocks:
        return ""
    return "\n\n".join(blocks) + "\n"


def _pypop_process_deprecation(_app, what, name, obj, _options, lines):
    """Sphinx `autodoc-process-docstring` handler.

    - `what`   : "module", "class", "function", etc.
    - `name`   : fully qualified name
    - `obj`    : the Python object
    - `options`: autodoc options
    - `lines`  : list of docstring lines (modifiable in place).
    """
    try:
        info = getattr(obj, "__pypop_deprecation__", None)
    except Exception:
        info = None

    if not info:
        print(f"[AutoAPI] nothing to do, can't inject {name}")
        return  # nothing to do

    print(f"[AutoAPI] Injecting deprecation into {name}")

    # Build replacement lines: place the deprecation directive at the top
    ver = info.get("version_warn", "1.4.0")
    new = info.get("new_name")
    deprecated_block = [f".. deprecated:: {ver}"]
    if new:
        # For functions use :func:, for classes you might want :class:
        # We don't know exact type reliably here; autodoc passes `what` so we can pick
        if what == "class":
            deprecated_block.append(f"   Use :class:`{new}` instead.")
        else:
            deprecated_block.append(f"   Use :func:`{new}` instead.")

    # Insert block at top of docstring lines with a blank line separator
    # Avoid duplicating if user already added a deprecated:: line themselves
    for line in lines:
        if line.strip().startswith(".. deprecated::"):
            return

    # Prepend in reverse order so final docstring starts with the directive
    for _i, line in enumerate(reversed([*deprecated_block, ""])):
        lines.insert(0, line)


def prepare_autoapi_index(app):
    """Substitute the top-level index using a template file with placeholders.

    Placeholders in api_index_override.rst:
        {{deprecations_block}}    -> substituted with _make_deprecations_block() output
        {{generated_api_index}}   -> substituted with the generated PyPop/index.rst content
    """
    autoapi_root = getattr(app.config, "autoapi_root", "")
    template_path = Path(app.srcdir) / "_static" / "api_index_override.rst"
    src_generated = Path(app.srcdir) / autoapi_root / "PyPop" / "index.rst"
    dst = Path(app.srcdir) / autoapi_root / "index.rst"

    print(
        f"[helpers]: generating API index from template {template_path}, "
        f"generated index {src_generated} → {dst}"
    )

    # --- read template ---
    template_content = template_path.read_text(encoding="utf-8")

    # --- read generated PyPop/index.rst content ---
    generated_content = ""
    if src_generated.exists():
        generated_content = src_generated.read_text(encoding="utf-8")
        generated_content = strip_first_title(generated_content)
        src_generated.unlink()  # prevent Sphinx from processing it separately

    # --- read deprecations ---
    deprecations_block = _make_deprecations_block()

    # --- substitute placeholders ---
    final_content = template_content
    final_content = final_content.replace("{{deprecations_block}}", deprecations_block)
    final_content = final_content.replace("{{generated_api_index}}", generated_content)

    # --- ensure destination exists ---
    dst.parent.mkdir(parents=True, exist_ok=True)

    # --- write final merged index.rst ---
    dst.write_text(final_content, encoding="utf-8")


def renumber_footnotes(app, exception):
    """Renumber all remaining LaTeX footnotes sequentially."""
    if exception or app.builder.name != "latex":
        return

    tex_files = Path(app.outdir).glob("*.tex")
    footnote_re = re.compile(r"(\\begin\{footnote\}\[(\d+)\])")

    for tex_file in tex_files:
        text = tex_file.read_text(encoding="utf-8")

        counter = 0

        def repl(_match):
            nonlocal counter
            counter += 1
            return f"\\begin{{footnote}}[{counter}]"

        new_text = footnote_re.sub(repl, text)
        tex_file.write_text(new_text, encoding="utf-8")
        print(f"[helpers] Renumbered {counter} footnotes in {tex_file.name}")


def patch_latex_files(app, exception):
    """Patch preamble and maketitle on a per-document basis."""
    if exception or app.builder.name != "latex":
        return

    tex_file_map = getattr(app, "tex_file_map", {})

    if not tex_file_map:
        tex_file_map = {}
        for doc in getattr(app.config, "latex_documents", []):
            # last element can be overrides dict
            overrides = doc[6] if len(doc) > 6 else {}
            target = Path(doc[1]).stem
            tex_file_map[target] = overrides

    tex_files = Path(app.outdir).glob("*.tex")

    for tex_file in tex_files:
        text = tex_file.read_text(encoding="utf-8")
        filename = tex_file.name

        for key, params in tex_file_map.items():
            if key in filename:
                # 1) Apply placeholder substitutions
                placeholders = params.get("placeholders", {}).copy()

                # --- Handle dynamic POINTSIZE substitution ---
                pointsize = placeholders.get("POINTSIZE")
                if pointsize:
                    try:
                        base = float(pointsize.replace("pt", ""))
                        small = base - 1
                        foot = base - 2
                        placeholders["POINTSIZE"] = (
                            r"\makeatletter"
                            f"\n\\renewcommand\\normalsize{{\\@setfontsize\\normalsize{{{base:.1f}pt}}{{{base + 1:.1f}pt}}}}"
                            f"\n\\renewcommand\\small{{\\@setfontsize\\small{{{small:.1f}pt}}{{{small + 1:.1f}pt}}}}"
                            f"\n\\renewcommand\\footnotesize{{\\@setfontsize\\footnotesize{{{foot:.1f}pt}}{{{foot + 1:.1f}pt}}}}"
                            "\n\\makeatother"
                        )
                    except ValueError:
                        print(
                            f"[helpers] Invalid POINTSIZE value in {filename}: {pointsize}"
                        )
                        placeholders["POINTSIZE"] = ""  # remove bad value
                else:
                    # Not set → replace placeholder with nothing
                    placeholders["POINTSIZE"] = ""

                for ph, val in placeholders.items():
                    text = text.replace(ph, val)

                # 2) Replace maketitle
                maketitle = params.get("maketitle", "")
                if maketitle:
                    text = re.sub(
                        r"^\\sphinxmaketitle\s*$",
                        lambda _m, maketitle=maketitle: maketitle.strip(),
                        text,
                        flags=re.MULTILINE,
                    )

                tex_file.write_text(text, encoding="utf-8")
                print(f"[helpers] Patched {filename}")
                break


def get_autoapi_dirs(package_name, fallback_dir):
    """Get the autoapi from a released/installed version."""
    if os.environ.get("PYPOP_DOCS_MODE", "") == "installed":
        try:
            spec = importlib.util.find_spec(package_name)
            if spec and spec.origin:
                installed_path = Path(spec.origin).parent
                print(
                    f"[helpers] Using installed {package_name} from: {installed_path}"
                )
                return [str(installed_path)]
            print(f"[helpers] {package_name} not found")
        except Exception as e:
            print(f"[helpers] Could not import installed package ({e})")
    # fallback
    fallback = str(Path(fallback_dir).resolve())
    print(f"[helpers] Using internal source directory: {fallback}")
    # ensure local sources are importable
    sys.path.insert(0, str(Path(fallback).parent))
    return [fallback]
