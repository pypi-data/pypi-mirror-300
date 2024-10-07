"""Development Utility Functions

Author, Copyright, and License
------------------------------
Copyright (c) 2023 Hauke Daempfling (haukex@zero-g.net)
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, https://www.igb-berlin.de/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/
"""
import os
import re
import sys
import ast
import enum
import argparse
import subprocess
from stat import S_IXUSR
from pathlib import Path
from typing import NamedTuple, Optional
from collections.abc import Sequence
from igbpyutils.file import Filename, cmdline_rglob, autoglob

class ResultLevel(enum.IntEnum):
    """A severity level enum for :class:`ScriptLibResult`.

    (Note the numeric values are mostly borrowed from :mod:`logging`.)"""
    INFO = 20
    NOTICE = 25
    WARNING = 30
    ERROR = 40

class ScriptLibFlags(enum.Flag):
    """Flags for :class:`ScriptLibResult`.

    .. warning::

        Always use the named flags, do not rely on the integer flag values staying constant,
        as they are automatically generated.
    """
    #: Whether the file has its execute bit set
    EXEC_BIT = enum.auto()
    #: Whether the file has a shebang line
    SHEBANG = enum.auto()
    #: Whether the file contains ``if __name__=='__main__': ...``
    NAME_MAIN = enum.auto()
    #: Whether the file contains statements that make it look like a script
    #: (i.e. anything that's not a ``def``, ``class``, etc.)
    SCRIPT_LIKE = enum.auto()

class ScriptLibResult(NamedTuple):
    """Result class for :func:`check_script_vs_lib`"""
    #: The file that was analyzed
    path :Path
    #: The severity of the result, see :class:`ResultLevel`
    level :ResultLevel
    #: A textual description of the result, with details
    message :str
    #: The individual results of the analysis, see :class:`ScriptLibFlags`
    flags :ScriptLibFlags

_IS_WINDOWS = sys.platform.startswith('win32')
_git_ls_tree_re = re.compile(r'''\A([0-7]+) blob [a-fA-F0-9]{40}\t(.+)(?:\Z|\n)''')

DEFAULT_SHEBANGS = (
    '#!/usr/bin/env python3',
    '#!/usr/bin/env python',
    '#!/usr/bin/python3',
    '#!/usr/bin/python',
    '#!/usr/local/bin/python3',
    '#!/usr/local/bin/python',
)

def check_script_vs_lib(path :Filename, *, known_shebangs :Sequence[str] = DEFAULT_SHEBANGS, exec_from_git :bool = False) -> ScriptLibResult:
    """This function analyzes a Python file to see whether it looks like a library or a script,
    and checks several features of the file for consistency.

    It checks the following points, each of which on their own would indicate the file is a script, but in certain combinations don't make sense.
    It checks whether the file...

    - has its execute bit set (ignored on Windows, unless ``exec_from_git`` is set)
    - has a shebang line (e.g. ``#!/usr/bin/env python3``, see also the ``known_shebangs`` parameter)
    - contains a ``if __name__=='__main__':`` line
    - contains statements other than ``class``, ``def``, etc. in the main body

    :param path: The name of the file to analyze.
    :param known_shebangs: You may provide your own list of shebang lines that this function will recognize here (each without the trailing newline).
    :param exec_from_git: If you set this to :obj:`True`, then instead of looking at the file's actual mode bits to determine whether the
        exec bit is set, the function will ask ``git`` for the mode bits of the file and use those.
    :return: A :class:`ScriptLibResult` object that indicates what was found and whether there are any inconsistencies.
    """
    pth = Path(path)
    flags = ScriptLibFlags(0)
    with pth.open(encoding='UTF-8') as fh:
        if not _IS_WINDOWS and os.stat(fh.fileno()).st_mode & S_IXUSR:
            flags |= ScriptLibFlags.EXEC_BIT
        source = fh.read()
    ignore_exec_bit = _IS_WINDOWS
    if exec_from_git:
        flags &= ~ScriptLibFlags.EXEC_BIT
        #TODO: This fails for newly added files - `git ls-files --stage` instead?
        res = subprocess.run(['git','ls-tree','HEAD',pth.name], cwd=pth.parent,
                             encoding='UTF-8', check=True, capture_output=True)
        assert not res.returncode and not res.stderr
        if m := _git_ls_tree_re.fullmatch(res.stdout):
            if m.group(2) != pth.name:
                raise RuntimeError(f"Unexpected git output, filename mismatch {res.stdout!r}")
            if int(m.group(1), 8) & S_IXUSR:
                flags |= ScriptLibFlags.EXEC_BIT
        else:
            raise RuntimeError(f"Failed to parse git output {res.stdout!r}")
        ignore_exec_bit = False
    shebang_line :str = ''
    if source.startswith('#!'):
        shebang_line = source[:source.index('\n')]
        flags |= ScriptLibFlags.SHEBANG
    why_scriptlike :list[str] = []
    for node in ast.iter_child_nodes(ast.parse(source, filename=str(pth))):
        # If(test=Compare(left=Name(id='__name__', ctx=Load()), ops=[Eq()], comparators=[Constant(value='__main__')])
        if (isinstance(node, ast.If) and isinstance(node.test, ast.Compare)  # pylint: disable=too-many-boolean-expressions
                and isinstance(node.test.left, ast.Name) and node.test.left.id=='__name__' and len(node.test.ops)==1
                and isinstance(node.test.ops[0], ast.Eq) and len(node.test.comparators)==1
                and isinstance(node.test.comparators[0], ast.Constant) and node.test.comparators[0].value=='__main__'):
            flags |= ScriptLibFlags.NAME_MAIN
        elif (not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                                    ast.Assign, ast.AnnAssign, ast.Assert))
              # docstring:
              and not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str))):
            why_scriptlike.append(f"{type(node).__name__}@L{node.lineno}")  # type: ignore[attr-defined]
    if why_scriptlike: flags |= ScriptLibFlags.SCRIPT_LIKE
    if flags&ScriptLibFlags.SHEBANG and shebang_line not in known_shebangs:
        return ScriptLibResult(pth, ResultLevel.WARNING, f"File has unrecognized shebang {shebang_line!r}", flags)
    if flags&ScriptLibFlags.NAME_MAIN and flags&ScriptLibFlags.SCRIPT_LIKE:
        return ScriptLibResult(pth, ResultLevel.ERROR, f"File has `if __name__=='__main__'` and looks like a script due to {', '.join(why_scriptlike)}", flags)
    elif not flags&ScriptLibFlags.SHEBANG and not flags&ScriptLibFlags.NAME_MAIN and not flags&ScriptLibFlags.SCRIPT_LIKE:
        # looks like a normal library
        if flags&ScriptLibFlags.EXEC_BIT:
            return ScriptLibResult(pth, ResultLevel.ERROR, f"File looks like a library but exec bit is set", flags)
        else:
            return ScriptLibResult(pth, ResultLevel.INFO, f"File looks like a normal library", flags)
    elif not flags&ScriptLibFlags.NAME_MAIN and not flags&ScriptLibFlags.SCRIPT_LIKE:
        assert flags&ScriptLibFlags.SHEBANG
        return ScriptLibResult(pth, ResultLevel.ERROR, f"File has shebang{' and exec bit' if flags&ScriptLibFlags.EXEC_BIT else ''} but seems to be missing anything script-like", flags)
    else:
        assert (flags&ScriptLibFlags.NAME_MAIN or flags&ScriptLibFlags.SCRIPT_LIKE) and not (flags&ScriptLibFlags.NAME_MAIN and flags&ScriptLibFlags.SCRIPT_LIKE)  # xor
        if (flags & ScriptLibFlags.EXEC_BIT or ignore_exec_bit) and flags&ScriptLibFlags.SHEBANG:
            if flags&ScriptLibFlags.SCRIPT_LIKE:
                return ScriptLibResult(pth, ResultLevel.NOTICE, f"File looks like a normal script (but could use `if __name__=='__main__'`)", flags)
            else:
                return ScriptLibResult(pth, ResultLevel.INFO, f"File looks like a normal script", flags)
        else:
            missing = ([] if flags & ScriptLibFlags.EXEC_BIT or ignore_exec_bit else ['exec bit']) + ([] if flags & ScriptLibFlags.SHEBANG else ['shebang'])
            assert missing
            why :str = ', '.join(why_scriptlike) if flags&ScriptLibFlags.SCRIPT_LIKE else "`if __name__=='__main__'`"
            return ScriptLibResult(pth, ResultLevel.ERROR, f"File looks like a script (due to {why}) but is missing {' and '.join(missing)}", flags)

def check_script_vs_lib_cli() -> None:
    """Command-line interface for :func:`check_script_vs_lib`.

    If the module and script have been installed correctly, you should be able to run ``py-check-script-vs-lib -h`` for help."""
    parser = argparse.ArgumentParser(description='Check Python Scripts vs. Libraries')
    parser.add_argument('-v', '--verbose', help="be verbose", action="store_true")
    parser.add_argument('-n', '--notice', help="show notices and include in issue count", action="store_true")
    parser.add_argument('-g', '--exec-git', help="get the exec bit from git", action="store_true")
    parser.add_argument('paths', help="the paths to check (directories searched recursively)", nargs='*')
    #TODO: Add an option to add known shebang lines
    args = parser.parse_args()
    issues :int = 0
    for path in cmdline_rglob(autoglob(args.paths)):
        if not path.is_file() or not path.suffix.lower()=='.py': continue
        result = check_script_vs_lib(path, exec_from_git=args.exec_git)
        if result.level>=ResultLevel.WARNING or args.verbose or args.notice and result.level>=ResultLevel.NOTICE:
            print(f"{result.level.name} {result.path}: {result.message}")
        if result.level>=ResultLevel.WARNING or args.notice and result.level>=ResultLevel.NOTICE:
            issues += 1
    parser.exit(issues)

def generate_coveragerc(*, minver :int, maxver :int, forver :Optional[int]=None, outdir :Optional[Path]=None, verbose :bool=False):
    """Generate ``.coveragerc3.X`` files for various Python 3 versions.

    These generated files provide tags such as ``cover-req-ge3.10`` and ``cover-req-lt3.10`` that can be used
    to exclude source code lines on ranges of Python versions. This tool is used within this project itself.
    In addition, the tags ``cover-linux``, ``cover-win32``, and ``cover-darwin`` are supplied based on ``sys.platform``
    for code for which coverage is only expected on those OSes (more such tags could be added in the future).
    Because the generated files use the ``exclude_also`` config option, Coverage.py 7.2.0 or greater is required.

    :param minver: The minimum Python minor version which to include in the generated tags, inclusive.
    :param maxver: The maximum Python minor version which to include in the generated tags, exclusive.
    :param forver: If specified, only a single ``.coverage3.X`` file for that minor version is generated,
        otherwise files are generated for all versions in the aforementioned range.
    :param outdir: The path into which to output the files. Defaults to the current working directory.
    :param verbose: If true, ``print`` a message for each file written.
    """
    #TODO: Investigate https://github.com/nedbat/coveragepy/issues/1699
    # https://github.com/asottile/covdefaults - does a bit too much for me
    # https://github.com/wemake-services/coverage-conditional-plugin
    versions = range(minver, maxver)
    if not versions:
        raise ValueError(f"No versions in range")
    if forver is not None and forver not in versions:
        raise ValueError(f"forver must be in the range minver to maxver")
    if not outdir: outdir = Path()
    for vc in versions if forver is None else (forver,):
        fn = outdir / f".coveragerc3.{vc}"
        with fn.open('x', encoding='ASCII', newline='\n') as fh:
            print(f"# Generated .coveragerc for Python 3.{vc}\n[report]\nexclude_also =", file=fh)
            if not sys.platform.startswith('linux'): print("    cover-linux", file=fh)
            if not sys.platform.startswith('win32'): print("    cover-win32", file=fh)
            if not sys.platform.startswith('darwin'): print("    cover-darwin", file=fh)
            for v in versions[1:]:
                print(f"    cover-req-" + re.escape(f"{'ge' if v>vc else 'lt'}3.{v}"), file=fh)
        if verbose: print(f"Wrote {fn}")

def _parsever(ver :str):
    if re.fullmatch(r'''\A[0-9]+\Z''', ver):
        return int(ver)
    elif m := re.fullmatch(r'''\A3\.([0-9]+)\Z''', ver):
        return int(m.group(1))
    else:
        raise ValueError(f"Failed to understand version number {ver!r}, must be \"3.X\" or minor version only")

def generate_coveragerc_cli():
    """Command-line interface for :func:`generate_coveragerc`.

    If the module and script have been installed correctly, you should be able to run ``gen-coveragerc -h`` for help."""
    parser = argparse.ArgumentParser(description='Generate .coveragerc3.X files')
    parser.add_argument('-q','--quiet', help="Don't output informational messages",action="store_true")
    parser.add_argument('-o','--outdir', help="Output directory")
    parser.add_argument('-f','--forver', metavar='VERSION', help="only generate for this version")
    parser.add_argument('minver', help="3.N minimum version (inclusive)")
    parser.add_argument('maxver', help="3.M maximum version (exclusive)")
    args = parser.parse_args()
    generate_coveragerc(minver=_parsever(args.minver), maxver=_parsever(args.maxver), verbose=not args.quiet,
        forver=_parsever(args.forver) if args.forver else None, outdir=Path(args.outdir) if args.outdir else None)
    parser.exit(0)
