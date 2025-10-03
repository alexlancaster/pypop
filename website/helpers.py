"""Customization and helper classes for conf.py."""

from pathlib import Path

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


class CustomLaTeXTranslator(SphinxLaTeXTranslator):
    """Customize the output in the LaTeX case."""

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


def prepare_autoapi_index(app):
    """Substitute the top-level index to be generated."""
    src_override = Path(app.srcdir) / "_static" / "api_index_override.rst"
    src_generated = Path(app.srcdir) / "autoapi" / "PyPop" / "index.rst"
    dst = Path(app.srcdir) / "autoapi" / "index.rst"

    # Read override content
    override_content = src_override.read_text(encoding="utf-8")

    # Read generated PyPop/index.rst content if it exists
    generated_content = ""
    if src_generated.exists():
        generated_content = src_generated.read_text(encoding="utf-8")
        # Delete the generated PyPop/index.rst so Sphinx doesn't process it separately
        src_generated.unlink()

    # Combine them: override first, then generated
    final_content = override_content + "\n\n" + generated_content

    # Ensure parent exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    # Write final merged index.rst
    dst.write_text(final_content, encoding="utf-8")
