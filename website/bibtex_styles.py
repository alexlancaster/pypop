from dataclasses import dataclass, field

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
    return BracketStyle(
        left="(",
        right=")",
    )


@dataclass
class MyReferenceStyle(AuthorYearReferenceStyle, ExtraYearReferenceStyle):
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
