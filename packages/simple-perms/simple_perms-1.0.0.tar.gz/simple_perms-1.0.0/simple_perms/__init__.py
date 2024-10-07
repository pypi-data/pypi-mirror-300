"""
Simplify \\*NIX Permissions
===========================

Please see the main documentation in ``README.md``.

Author, Copyright, and License
------------------------------

Copyright (c) 2022-2024 Hauke Dämpfling (haukex@zero-g.net)
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, https://www.igb-berlin.de/

This library is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see https://www.gnu.org/licenses/
"""
import os
import stat
import argparse
from pathlib import Path
from typing import Optional

def suggest_perms(st_mode :int, *, group_write :Optional[bool] = None) -> tuple[int, int]:
    """Given a set of file mode bits (:attr:`~os.stat_result.st_mode`), this function suggests new permissions
    from a small set of "simple" permissions (0o444, 0o555, 0o644, 0o755, 0o664, 0o775).

    :param st_mode: The original mode bits *including* the file type information.
        Usually, you would take this from :attr:`os.stat_result.st_mode` as returned by :func:`os.lstat` or :meth:`pathlib.Path.lstat`.

    :param group_write: Whether the suggestion should have the group write bit set.
        Note that the group write bit is *never* suggested unless the original has the user write bit set.

        - When :obj:`None` (the default), the suggestion is based on the original group write bit.
        - When :obj:`False`, the suggestion never has the group write bit set.
        - When :obj:`True`, the suggestion always has the group write bit set.

    :return: A tuple consisting of the file's original permissions and suggested permissions to use instead,
        based on the arguments to this function, the file's original user permission bits, and whether it is a directory or not.
        The two values may be equal indicating that no change is suggested. No changes are ever suggested for symbolic links.
    """
    perms = stat.S_IMODE(st_mode)
    # don't suggest changes for links
    if stat.S_ISLNK(st_mode):
        return perms, perms
    # base permissions are "all read"
    new_perms = stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH
    # execute permissions for directories or when user turns on their execute bit
    if stat.S_ISDIR(st_mode) | ( st_mode & stat.S_IXUSR ):
        new_perms |= stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH
    # transfer over user write permissions
    if st_mode & stat.S_IWUSR:
        new_perms |= stat.S_IWUSR
        # group write gets set when explicitly requested,
        if group_write:
            new_perms |= stat.S_IWGRP
        # or transferred over when it is set to `None` (don't care)
        # (note this is in a separate branch to make code coverage obvious)
        elif group_write is None and st_mode & stat.S_IWGRP:
            new_perms |= stat.S_IWGRP
    assert not (new_perms & stat.S_IWOTH) and new_perms in (0o444, 0o555, 0o644, 0o755, 0o664, 0o775)  # triple-check
    return perms, new_perms

def _get_umask():
    umask = os.umask(0)
    os.umask(umask)
    assert os.umask(umask) == umask
    return umask

def _arg_parser():
    parser = argparse.ArgumentParser('simple-perms', description='Check for Simple Permissions')
    parser.add_argument('-v', '--verbose', action="store_true", help="list all files")
    parser.add_argument('-r', '--recurse', action='store_true', help="recurse into directories")
    parser.add_argument('-m', '--modify', action="store_true", help="automatically modify files' permissions")
    parser.add_argument('-g', '--group-write', action="store_true", default=None, help="the group should have write permission")
    parser.add_argument('-G', '--no-group-write', dest='group_write', action="store_false", default=None,
                        help="the group should never have write permission")
    parser.add_argument('--ignore-group-write', dest='group_write', action="store_const", const=None,
                        help="use original group write permission (default)")
    parser.add_argument('-a', '--add', help="add these permission bits to all files/dirs (octal)")
    parser.add_argument('-d', '--add-dir', help="add these permission bits to dirs (octal)")
    parser.add_argument('-f', '--add-file', help="add these permission bits to non-dirs (octal)")
    #TODO: allow turning on --umask via an environment variable
    parser.add_argument('-k', '--umask', action='store_true', help="apply os.umask() to suggested permission bits")
    # NOTE in the previous version from igbpyutils, the following was -u|--umask, so that is a minor breaking change
    parser.add_argument('-u', '--mask', help="mask (remove) these permission bits from suggestion (octal)")
    parser.add_argument('paths', nargs='+', help="the files to check")
    # Possible To-Do for Later: A -s/--silence-errors option to ignore FileNotFoundErrors here
    # Possible To-Do for Later: --exclude using https://pypi.org/project/wcmatch/ ?
    return parser

def main(argv=None) -> None:
    """Command-line interface for :func:`simple_perms`.

    If this module and script have been installed correctly, you should be able to run ``simple-perms -h`` for help."""
    parser = _arg_parser()
    args = parser.parse_args(argv)
    issues :int = 0
    add_perm = stat.S_IMODE(int(args.add, 8)) if args.add else 0
    add_dir_perm = stat.S_IMODE(int(args.add_dir, 8)) if args.add_dir else 0
    add_file_perm = stat.S_IMODE(int(args.add_file, 8)) if args.add_file else 0
    mask :int = 0
    if args.mask:
        mask |= stat.S_IMODE(int(args.mask, 8))
    if args.umask:
        # Possible To-Do for Later: add tests for --umask ?
        mask |= _get_umask()  # pragma: no cover
    def _paths(paths, recurse :bool):
        for pth in paths:
            p = Path(pth)
            yield p
            if recurse and p.is_dir():
                yield from p.rglob('*')
    for path in _paths(args.paths, args.recurse):
        mode = path.lstat().st_mode
        perm, sugg = suggest_perms(mode, group_write=args.group_write)
        if not stat.S_ISLNK(mode):
            sugg &= ~mask
            sugg |= add_perm
            sugg |= add_dir_perm if stat.S_ISDIR(mode) else add_file_perm
        if perm != sugg:
            print(f"{stat.filemode(mode)} => {stat.filemode(stat.S_IFMT(mode)|stat.S_IMODE(sugg))} {path}")
            if args.modify:
                os.chmod(path, sugg)
            else:
                issues += 1
        elif args.verbose:
            print(f"{stat.filemode(mode)} ok {stat.filemode(mode)} {path}")
    parser.exit(issues)
