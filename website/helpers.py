"""Customization and helper classes for conf.py."""

import importlib.util
import os
import re
import sys
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


def prepare_autoapi_index(app):
    """Substitute the top-level index to be generated."""
    # don't hardcode, get this from config
    autoapi_root = getattr(app.config, "autoapi_root", "")
    src_override = Path(app.srcdir) / "_static" / "api_index_override.rst"
    src_generated = Path(app.srcdir) / autoapi_root / "PyPop" / "index.rst"
    dst = Path(app.srcdir) / autoapi_root / "index.rst"

    print(
        f"[helpers]: replace index: concatenate {src_override} with {src_generated} and put output in {dst}"
    )

    # Read override content
    override_content = src_override.read_text(encoding="utf-8")

    # Read generated PyPop/index.rst content if it exists
    generated_content = ""
    if src_generated.exists():
        generated_content = src_generated.read_text(encoding="utf-8")
        # FIXME: get ride of first title in the generated content, slightly hacky
        generated_content = strip_first_title(generated_content)
        # Delete the generated PyPop/index.rst so Sphinx doesn't process it separately
        src_generated.unlink()

    # Combine them: override first, then generated
    final_content = override_content + "\n\n" + generated_content

    # Ensure parent exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    # Write final merged index.rst
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
                    f"[get_autoapi_dirs] Using installed {package_name} from: {installed_path}"
                )
                return [str(installed_path)]
        except Exception as e:
            print(f"[helpers] Could not import installed package ({e})")
    # fallback
    fallback = str(Path(fallback_dir).resolve())
    print(f"[get_autoapi_dirs] Using fallback source directory: {fallback}")
    # ensure local sources are importable
    sys.path.insert(0, str(Path(fallback).parent))
    return [fallback]
