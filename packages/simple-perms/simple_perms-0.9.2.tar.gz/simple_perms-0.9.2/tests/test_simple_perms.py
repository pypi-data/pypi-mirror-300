"""Tests for :mod:`simple_perms`.

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
import sys
import stat
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from tempfile import TemporaryDirectory
import simple_perms as uut

class SimplePermsTestCase(unittest.TestCase):

    def test_suggest_perms(self):
        testcases = (
            # mode, sugg,  dir,   gw=F   +dir,  gw=T   +dir
            (0o444, 0o444, 0o555, 0o444, 0o555, 0o444, 0o555),
            (0o555, 0o555, 0o555, 0o555, 0o555, 0o555, 0o555),
            (0o644, 0o644, 0o755, 0o644, 0o755, 0o664, 0o775),
            (0o755, 0o755, 0o755, 0o755, 0o755, 0o775, 0o775),
            (0o664, 0o664, 0o775, 0o644, 0o755, 0o664, 0o775),
            (0o775, 0o775, 0o775, 0o755, 0o755, 0o775, 0o775),
            (0o000, 0o444, 0o555, 0o444, 0o555, 0o444, 0o555),  # 0 User bits
            (0o077, 0o444, 0o555, 0o444, 0o555, 0o444, 0o555),  # 0
            (0o100, 0o555, 0o555, 0o555, 0o555, 0o555, 0o555),  # X
            (0o177, 0o555, 0o555, 0o555, 0o555, 0o555, 0o555),  # X
            (0o200, 0o644, 0o755, 0o644, 0o755, 0o664, 0o775),  # W
            (0o277, 0o664, 0o775, 0o644, 0o755, 0o664, 0o775),  # W
            (0o400, 0o444, 0o555, 0o444, 0o555, 0o444, 0o555),  # R
            (0o477, 0o444, 0o555, 0o444, 0o555, 0o444, 0o555),  # R
            (0o644|stat.S_ISUID|stat.S_ISGID|stat.S_ISVTX,
                    0o644, 0o755, 0o644, 0o755, 0o664, 0o775),  # noqa: E127
        )
        for mode,sugg,isdr,nogw,gwfd,gwon,gwtd in testcases:
            for m in (sugg,isdr,nogw,gwfd,gwon,gwtd):  # self-test our test cases
                self.assertIn( m, (0o444, 0o555, 0o644, 0o755, 0o664, 0o775) )
                self.assertFalse( m&stat.S_IWOTH )
            self.assertEqual( (mode,sugg), uut.suggest_perms(mode|stat.S_IFREG) )
            self.assertEqual( (mode,isdr), uut.suggest_perms(mode|stat.S_IFDIR) )
            self.assertEqual( (mode,mode), uut.suggest_perms(mode|stat.S_IFLNK) )
            self.assertEqual( (mode,sugg), uut.suggest_perms(mode|stat.S_IFREG, group_write=None ) )
            self.assertEqual( (mode,isdr), uut.suggest_perms(mode|stat.S_IFDIR, group_write=None ) )
            self.assertEqual( (mode,mode), uut.suggest_perms(mode|stat.S_IFLNK, group_write=None ) )
            self.assertEqual( (mode,nogw), uut.suggest_perms(mode|stat.S_IFREG, group_write=False) )
            self.assertEqual( (mode,gwfd), uut.suggest_perms(mode|stat.S_IFDIR, group_write=False) )
            self.assertEqual( (mode,mode), uut.suggest_perms(mode|stat.S_IFLNK, group_write=False) )
            self.assertEqual( (mode,gwon), uut.suggest_perms(mode|stat.S_IFREG, group_write=True ) )
            self.assertEqual( (mode,gwtd), uut.suggest_perms(mode|stat.S_IFDIR, group_write=True ) )
            self.assertEqual( (mode,mode), uut.suggest_perms(mode|stat.S_IFLNK, group_write=True ) )

    def test_simple_perms_cli(self):  # pylint: disable=too-many-statements
        with TemporaryDirectory() as td:
            tdr = Path(td)
            os.chmod(tdr, 0o755)
            f_one = tdr / 'one.txt'
            f_one.touch()
            os.chmod(f_one, 0o644)
            f_two = tdr / 'two.txt'
            f_two.touch()
            os.chmod(f_two, 0o660)
            s_lnk = tdr / 'link.txt'
            os.symlink(f_one, s_lnk)
            sym_mode = stat.filemode(s_lnk.lstat().st_mode)  # apparently different on OSX and Linux

            # basic tests

            out = StringIO()
            sys.argv = ["simple-perms", "-r", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-rw---- => -rw-rw-r-- {f_two}",
            ] )

            out = StringIO()
            sys.argv = ["simple-perms", "-rv", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-r--r-- ok -rw-r--r-- {f_one}",
                f"-rw-rw---- => -rw-rw-r-- {f_two}",
                f"drwxr-xr-x ok drwxr-xr-x {tdr}",
                f"{sym_mode} ok {sym_mode} {s_lnk}",
            ] )

            out = StringIO()
            sys.argv = ["simple-perms", "-v", str(tdr), str(f_one), str(f_two), str(s_lnk)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-r--r-- ok -rw-r--r-- {f_one}",
                f"-rw-rw---- => -rw-rw-r-- {f_two}",
                f"drwxr-xr-x ok drwxr-xr-x {tdr}",
                f"{sym_mode} ok {sym_mode} {s_lnk}",
            ] )

            # group-write tests

            # this test is the same as the above, but with --ignore-group-write specified explicitly
            out = StringIO()
            sys.argv = ["simple-perms", "-r", "--ignore-group-write", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-rw---- => -rw-rw-r-- {f_two}",
            ] )

            out = StringIO()
            sys.argv = ["simple-perms", "-r", "--no-group-write", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-rw---- => -rw-r--r-- {f_two}",
            ] )

            os.chmod(f_two, 0o600)

            out = StringIO()
            sys.argv = ["simple-perms", "-r", "--ignore-group-write", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw------- => -rw-r--r-- {f_two}",
            ] )

            out = StringIO()
            sys.argv = ["simple-perms", "-r", "--group-write", str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(3)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw------- => -rw-rw-r-- {f_two}",
                f"-rw-r--r-- => -rw-rw-r-- {f_one}",
                f"drwxr-xr-x => drwxrwxr-x {tdr}",
            ] )

            # a few masking tests

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-u', '077', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(2)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-r--r-- => -rw------- {f_one}",
                f"drwxr-xr-x => drwx------ {tdr}",
            ] )

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-u', '027', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(3)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw------- => -rw-r----- {f_two}",
                f"-rw-r--r-- => -rw-r----- {f_one}",
                f"drwxr-xr-x => drwxr-x--- {tdr}",
            ] )

            # verbose tests

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-v', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(1)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw------- => -rw-r--r-- {f_two}",
                f"-rw-r--r-- ok -rw-r--r-- {f_one}",
                f"drwxr-xr-x ok drwxr-xr-x {tdr}",
                f"{sym_mode} ok {sym_mode} {s_lnk}",
            ] )

            # modification tests

            self.assertEqual( stat.S_IMODE(f_one.lstat().st_mode), 0o644 )
            self.assertEqual( stat.S_IMODE(f_two.lstat().st_mode), 0o600 )

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-m', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(0)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw------- => -rw-r--r-- {f_two}",
            ] )

            self.assertEqual( stat.S_IMODE(f_one.lstat().st_mode), 0o644 )
            self.assertEqual( stat.S_IMODE(f_two.lstat().st_mode), 0o644 )

            os.chmod(f_one, 0o441)
            os.chmod(f_two, stat.S_IXUSR)
            d_thr = tdr/'three'
            d_thr.mkdir()
            os.chmod(d_thr, 0o600)
            d_fou = tdr/'four'
            d_fou.mkdir()
            os.chmod(d_fou, 0o111)

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-m', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(0)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"---x------ => -r-xr-xr-x {f_two}",
                f"-r--r----x => -r--r--r-- {f_one}",
                f"d--x--x--x => dr-xr-xr-x {d_fou}",
                f"drw------- => drwxr-xr-x {d_thr}",
            ] )

            self.assertEqual( stat.S_IMODE(  tdr.lstat().st_mode), 0o755 )
            self.assertEqual( stat.S_IMODE(f_one.lstat().st_mode), 0o444 )
            self.assertEqual( stat.S_IMODE(f_two.lstat().st_mode), 0o555 )
            self.assertEqual( stat.S_IMODE(d_thr.lstat().st_mode), 0o755 )
            self.assertEqual( stat.S_IMODE(d_fou.lstat().st_mode), 0o555 )

            os.chmod(f_one, 0o641)

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-mg', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(0)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-rw-r----x => -rw-rw-r-- {f_one}",
                f"drwxr-xr-x => drwxrwxr-x {tdr}",
                f"drwxr-xr-x => drwxrwxr-x {d_thr}",
            ] )

            self.assertEqual( stat.S_IMODE(  tdr.lstat().st_mode), 0o775 )
            self.assertEqual( stat.S_IMODE(f_one.lstat().st_mode), 0o664 )
            self.assertEqual( stat.S_IMODE(f_two.lstat().st_mode), 0o555 )
            self.assertEqual( stat.S_IMODE(d_thr.lstat().st_mode), 0o775 )
            self.assertEqual( stat.S_IMODE(d_fou.lstat().st_mode), 0o555 )

            out = StringIO()
            sys.argv = ["simple-perms", "-r", '-m', '-u077', '-a004', '-d2050', '-f001', str(tdr)]
            with (redirect_stdout(out), patch('argparse.ArgumentParser.exit') as mock):
                uut.main()
            mock.assert_called_once_with(0)
            self.assertEqual( sorted(out.getvalue().splitlines()), [
                f"-r-xr-xr-x => -r-x---r-x {f_two}",
                f"-rw-rw-r-- => -rw----r-x {f_one}",
                f"dr-xr-xr-x => dr-xr-sr-- {d_fou}",
                f"drwxrwxr-x => drwxr-sr-- {tdr}",
                f"drwxrwxr-x => drwxr-sr-- {d_thr}",
            ] )

            self.assertEqual( stat.S_IMODE(  tdr.lstat().st_mode), 0o2754 )
            self.assertEqual( stat.S_IMODE(f_one.lstat().st_mode), 0o0605 )
            self.assertEqual( stat.S_IMODE(f_two.lstat().st_mode), 0o0505 )
            self.assertEqual( stat.S_IMODE(d_thr.lstat().st_mode), 0o2754 )
            self.assertEqual( stat.S_IMODE(d_fou.lstat().st_mode), 0o2554 )

        get_msk = uut._get_umask  # pyright: ignore [reportPrivateUsage]  # pylint: disable=protected-access
        self.assertEqual( os.umask(get_msk()), get_msk() )
        self.assertEqual( os.umask(get_msk()), get_msk() )
