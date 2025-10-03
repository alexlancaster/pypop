"""Custom classes for bibtex styles."""

from dataclasses import dataclass, field

import pybtex.plugin
import sphinxcontrib.bibtex.plugin
from pybtex.style.formatting.alpha import Style as AlphaStyle
from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year import AuthorYearReferenceStyle
from sphinxcontrib.bibtex.style.referencing.extra_year import ExtraYearReferenceStyle
from sphinxcontrib.bibtex.style.template import (
    join2,
    post_text,
    pre_text,
    reference,
    year,
)


def bracket_style():
    """Use round brackets."""
    return BracketStyle(
        left="(",
        right=")",
    )


@dataclass
class MyReferenceStyle(AuthorYearReferenceStyle, ExtraYearReferenceStyle):
    """Overwrite the default square brackets with round-brackets style.

    Allow for pre and post-text for :cite:year and :cite:yearpar
    remove space between citation and post-text, so that it supports
    output like: "Author (2024a, 2024b)"

    """

    bracket_parenthetical: BracketStyle = field(default_factory=bracket_style)
    bracket_textual: BracketStyle = field(default_factory=bracket_style)
    bracket_author: BracketStyle = field(default_factory=bracket_style)
    bracket_label: BracketStyle = field(default_factory=bracket_style)
    bracket_year: BracketStyle = field(default_factory=bracket_style)

    # override Separator between citation and post-text to drop comma and space
    post_text_sep: str = ""

    def inner(self, role_name):
        # introspection to decide which parent class method to call
        if role_name in {"year", "yearpar"}:
            print("MyReferenceStyle:", role_name)
            # append the pre and post text (original file does not do this)
            return join2(sep1=self.pre_text_sep, sep2=self.post_text_sep)[
                pre_text,
                reference[year],
                post_text,
            ]
        # call the inner method for AuthorYearReferenceStyle
        return super(AuthorYearReferenceStyle, self).inner(role_name)


sphinxcontrib.bibtex.plugin.register_plugin(
    "sphinxcontrib.bibtex.style.referencing", "author_year_round", MyReferenceStyle
)

# FIXME: should move this to top - currently doesn't work
from pybtex.style.template import field, first_of, optional, sentence  # noqa: E402


class AlphaInitialsStyle(AlphaStyle):
    """Custom bibligraphy style."""

    name = "alpha-initials"
    default_name_style = "lastfirst"  # put the lastname first
    default_label_style = "alpha"  # 'number' or 'alpha'
    default_sorting_style = "author_year_title"

    def __init__(self, **kwargs):
        super().__init__(abbreviate_names=True, **kwargs)  # abbreviate initials

    def format_web_refs(self, e):
        # try for DOI, PubMed or EPrint first, only include URL if not present
        return first_of[
            sentence[
                optional[self.format_eprint(e)],
                optional[self.format_pubmed(e)],
                optional[self.format_doi(e)],
            ],
            optional[
                self.format_url(e), optional[" (accessed on ", field("urldate"), ")"]
            ],
        ]


pybtex.plugin.register_plugin(
    "pybtex.style.formatting", "alpha-initials", AlphaInitialsStyle
)
