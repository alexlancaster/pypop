# This file is part of PyPop

# Copyright (C) 2023
# PyPop contributors

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

# IN NO EVENT SHALL CONTRIBUTORS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF CONTRIBUTORS HAVE BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING
# DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS
# IS". CONTRIBUTORS HAVE NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
"""Command-line interface for PyPop scripts."""

from argparse import (
    Action,
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
)
from pathlib import Path

from PyPop import platform_info  # global info
from PyPop.citation import citation_output_formats  # and citation formats


class _PyPopFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    """Class for combining both kinds of formats."""


class CitationAction(Action):
    """A custom ``argparse`` ``Citation`` action to read the appropriate citation file format."""

    def __call__(self, parser, _, values, _option_string=None):
        citation_format = values or "apalike"
        citation_file_name = f"citation/CITATION.{citation_format}"

        try:  # looking in installed package, need to do lazy import
            from importlib.resources import files  # noqa: PLC0415

            citation_file = files("PyPop").joinpath(citation_file_name)
            citation_text = citation_file.read_text()
        except (
            ModuleNotFoundError,
            ImportError,
            FileNotFoundError,
        ):  # fallback to using backport if not found, needs a lazy import
            try:
                from importlib_resources import files  # noqa: PLC0415

                citation_file = files("PyPop").joinpath(citation_file_name)
                citation_text = citation_file.read_text()
            except (
                ModuleNotFoundError,
                ImportError,
                FileNotFoundError,
            ):  # fallback to looking in top-level directory if running from repo
                top_level_dir = Path(__file__).resolve().parent.parent.parent
                citation_file = top_level_dir / "CITATION.cff"  # only output CFF

                if citation_file.exists():
                    print("only CITATION.cff is available")
                    print()
                    citation_text = citation_file.read_text()
                else:
                    print("could not locate the specified citation format.")
                    parser.exit()

        print(citation_text)
        parser.exit()  # exit after printing the file


def get_parent_cli(version="", copyright_message=""):
    """Command-line options common to all scripts.

    Args:
        version (str): Software version.
        copyright_message (str): Override the copyright message.

    Returns:
        tuple: A tuple of:
            - parent_parser (argparse.ArgumentParser): The base parser.
            - ihwg_args (tuple): Options for the IHWG module.
            - phylip_args (tuple): Options for the Phylip module.
            - common_args (tuple): Common options.
            - prefix_tsv_args (tuple): TSV prefix options.
    """
    parent_parser = ArgumentParser(add_help=False)

    # define function arguments as signatures - need to be added in child parser as part of the selection logic
    common_args = [
        (
            ["-h", "--help"],
            {"action": "help", "help": "show this help message and exit"},
        ),
        (
            ["--citation"],
            {
                "help": "generate citation to PyPop for this version of PyPop",
                "action": CitationAction,
                "nargs": "?",
                "choices": citation_output_formats,
                "default": "apalike",
            },
        ),
        (
            ["-o", "--outputdir"],
            {
                "help": "put output in directory ``OUTPUTDIR``",
                "required": False,
                "type": Path,
                "default": None,
            },
        ),
        (
            ["-V", "--version"],
            {
                "action": "version",
                "version": f"%(prog)s {version}\n{platform_info}\n{copyright_message}",
            },
        ),
    ]

    # Common logging options
    logging_args = [
        (
            ["-d", "--debug"],
            {
                "help": "enable debugging output (sets log level to ``DEBUG`` and overrides config file setting)",
                "action": "store_true",
                "required": False,
                "default": False,
            },
        ),
        (
            ["--log-level"],
            {
                "help": """
set log level (overrides ``-d``); one of: ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``

.. versionadded:: 1.4.0
                """,
                "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                "default": None,
            },
        ),
        (
            ["--log-file"],
            {
                "help": """
write logs to ``LOGFILE`` instead of ``stdout``

.. versionadded:: 1.4.0
                """,
                "metavar": "LOGFILE",
                "default": None,
            },
        ),
    ]

    # Merge logging options into common args
    common_args.extend(logging_args)

    ihwg_args = (
        "--enable-ihwg",
        {
            "help": "enable 13th IWHG workshop populationdata default headers",
            "action": "store_true",
            "required": False,
            "default": False,
        },
    )
    phylip_args = (
        "--enable-phylip",
        {
            "help": "enable generation of PHYLIP ``.phy`` files",
            "action": "store_true",
            "required": False,
            "default": False,
        },
    )
    prefix_tsv_args = (
        ["-p", "--prefix-tsv"],
        {
            "help": "append ``PREFIX_TSV`` to the output TSV files",
            "metavar": "PREFIX_TSV",
            "required": False,
            "default": None,
        },
    )

    return parent_parser, ihwg_args, phylip_args, common_args, prefix_tsv_args


def get_pypop_cli(version="", copyright_message=""):
    """Command-line options for ``pypop`` script.

    Args:
        version (str): software version
        copyright_message (str): override the copyright message

    Returns:
        argparse.ArgumentParser: parser for ``pypop``
    """
    parent_parser, ihwg_args, phylip_args, common_args, prefix_tsv_args = (
        get_parent_cli(version=version, copyright_message=copyright_message)
    )
    pypop_parser = ArgumentParser(
        prog="pypop",
        parents=[parent_parser],
        add_help=False,
        description="""Process and run population genetics statistics on one or more ``POPFILE`` s.
Expects to find a configuration file called ``config.ini`` in the
current directory""",
        epilog=copyright_message,
        formatter_class=_PyPopFormatter,
    )

    add_pypop = pypop_parser.add_argument_group("Options for pypop").add_argument
    for arg in common_args:
        add_pypop(*arg[0], **arg[1])

    add_pypop(
        "-c",
        "--config",
        help="select config file",
        required=False,
        default="config.ini",
    )
    add_pypop(
        "-m",
        "--testmode",
        help="run PyPop in test mode for unit testing",
        action="store_true",
        required=False,
        default=False,
    )
    add_pypop(
        "-x",
        "--xsl",
        help="override the default XSLT translation with ``XSLFILE``",
        metavar="XSLFILE",
        required=False,
        default=None,
    )

    add_tsv = pypop_parser.add_argument_group(
        "TSV output options",
        "Note that ``--enable-*`` and ``--prefix-tsv`` options are only valid if ``--enable-tsv``/``-t`` is also supplied",
    ).add_argument
    add_tsv(
        "-t",
        "--enable-tsv",
        help="generate TSV output files (aka run ``popmeta``)",
        action="store_true",
        required=False,
        default=False,
    )
    add_tsv(ihwg_args[0], **ihwg_args[1])
    add_tsv(phylip_args[0], **phylip_args[1])
    add_tsv(*prefix_tsv_args[0], **prefix_tsv_args[1])

    gp_input = pypop_parser.add_argument_group("Mutually exclusive input options")
    add_input = gp_input.add_mutually_exclusive_group(required=True).add_argument
    add_input(
        "-i",
        "--interactive",
        help="run in interactive mode, prompting user for file names",
        action="store_true",
        default=False,
    )
    add_input(
        "-f",
        "--filelist",
        help="file containing list of files (one per line) to process. files are resolved relative to ``FILELIST``, unless absolute. mutually exclusive with supplying ``POPFILE``)",
        default=None,
    )
    add_input(
        "popfiles",
        metavar="POPFILE",
        help="input population (``.pop``) file(s)",
        nargs="*",
        default=[],
    )

    return pypop_parser


def get_popmeta_cli(version="", copyright_message=""):
    """Command-line options for ``popmeta`` script.

    Args:
        version (str): software version
        copyright_message (str): override the copyright message

    Returns:
        argparse.ArgumentParser: parser for ``popmeta``
    """
    parent_parser, ihwg_args, phylip_args, common_args, prefix_tsv_args = (
        get_parent_cli(version=version, copyright_message=copyright_message)
    )
    popmeta_parser = ArgumentParser(
        prog="popmeta",
        parents=[parent_parser],
        add_help=False,
        epilog=copyright_message,
        description="""Processes ``XMLFILEs`` and generates 'meta'-analyses. ``XMLFILE`` are
expected to be the XML output files taken from runs of ``pypop``.  Will
skip any XML files that are not well-formed XML.""",
        formatter_class=_PyPopFormatter,
    )

    popmeta_parser.add_argument(
        "xmlfiles",
        metavar="XMLFILE",
        help="XML (``.xml``) file(s) generated by pypop runs",
        nargs="+",
        default=[],
    )

    add_popmeta = popmeta_parser.add_argument_group("Options for popmeta").add_argument
    for arg in common_args:
        add_popmeta(*arg[0], **arg[1])

    add_popmeta(*prefix_tsv_args[0], **prefix_tsv_args[1])

    add_popmeta(
        "--disable-tsv",
        help="disable generation of ``.tsv`` TSV files",
        action="store_false",
        dest="generate_tsv",
        required=False,
        default=True,
    )
    add_popmeta(
        "--output-meta",
        help="dump the meta output file to ``stdout``, ignore xslt file",
        action="store_true",
        required=False,
        default=False,
    )
    add_popmeta(
        "-x",
        "--xsldir",
        help="use specified directory to find meta XSLT",
        metavar="XSLDIR",
        required=False,
        default=None,
    )
    add_popmeta(ihwg_args[0], **ihwg_args[1])

    xor_options = popmeta_parser.add_argument_group(
        "Mutually exclusive popmeta options"
    )
    add_xor_arg = xor_options.add_mutually_exclusive_group(required=False).add_argument
    add_xor_arg(phylip_args[0], **phylip_args[1])
    add_xor_arg(
        "-b",
        "--batchsize",
        help="process in batches of size total/``FACTOR`` rather than all at once, by default do separately (``batchsize=0``)",
        type=int,
        metavar="FACTOR",
        required=False,
        default=0,
    )

    return popmeta_parser
