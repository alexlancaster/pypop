#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2024.
# All Rights Reserved.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING
# DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS
# IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

import shutil
from pathlib import Path

citation_output_formats = [
    "apalike",
    "bibtex",
    "endnote",
    "ris",
    "codemeta",
    "cff",
    "schema.org",
    "zenodo",
]


def convert_citation_formats(build_lib, citation_path):
    from cffconvert import Citation

    # target directory for the CITATION file within the build directory
    target_dir = Path(build_lib) / "PyPop" / "citation"

    # create the citation directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(citation_path, target_dir)

    # load the CITATION.cff content
    with open(citation_path) as f:
        cff = Citation(cffstr=f.read())

    # remove 'cff' from generated list - since we don't generate that
    citation_output_formats.remove("cff")

    for fmt in citation_output_formats:
        # use getattr to get the method based on the format string, remove periods in methods
        convert_method = getattr(cff, f"as_{fmt.replace('.', '')}", None)
        if callable(convert_method):
            converted_content = convert_method()

            # save the converted output (e.g., as CITATION.json)
            with open(target_dir / f"CITATION.{fmt}", "w") as f:
                f.write(converted_content)
        else:
            print(f"Conversion format '{fmt}' not supported.")


if __name__ == "__main__":
    convert_citation_formats("src", "CITATION.cff")
