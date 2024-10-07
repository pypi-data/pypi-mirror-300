# Simplify \*NIX Permissions

This package primarily provides a command-line script, `simple-perms`, which suggests and can optionally apply
permission bits from a small set of “simple” permissions (0o444, 0o555, 0o644, 0o755, 0o664, 0o775) based on
the original file’s permissions and type, as follows.

1. The basic suggested permission bits are 0o444.
2. If the file is a directory, or it has its user execute bit set, the suggested permissions are 0o555.
3. If the file has its user write bit set, then the suggested permissions are 0o644 or 0o755.
4. If the file has its user write bit set, then the suggested group write permissions (0o664 or 0o775) depend on the options:
   - No option or `--ignore-group-write`: The suggestion is based on the original group write bit.
   - `--group-write`: The suggestion always has the group write bit set.
   - `--no-group-write`: The suggestion never has the group write bit set.
5. Additionally, the command-line interface allows the setting and masking of permission bits.

No changes are ever suggested for symbolic links.

The motivation for this tool comes from a few different needs, such as:

- When copying files from FAT media, they will often have 0o777 permissions
- When working on a website while having a restrictive umask, files may not be accessible to the webserver

## Command-Line Interface

```default
usage: simple-perms [-h] [-v] [-r] [-m] [-g] [-G] [--ignore-group-write] [-a ADD] [-d ADD_DIR] [-f ADD_FILE] [-k] [-u MASK] paths [paths ...]

Check for Simple Permissions

positional arguments:
  paths                 the files to check

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         list all files
  -r, --recurse         recurse into directories
  -m, --modify          automatically modify files' permissions
  -g, --group-write     the group should have write permission
  -G, --no-group-write  the group should never have write permission
  --ignore-group-write  use original group write permission (default)
  -a ADD, --add ADD     add these permission bits to all files/dirs (octal)
  -d ADD_DIR, --add-dir ADD_DIR
                        add these permission bits to dirs (octal)
  -f ADD_FILE, --add-file ADD_FILE
                        add these permission bits to non-dirs (octal)
  -k, --umask           apply os.umask() to suggested permission bits
  -u MASK, --mask MASK  mask (remove) these permission bits from suggestion (octal)
```

## Functions

### simple_perms.suggest_perms(st_mode: [int](https://docs.python.org/3/library/functions.html#int), \*, group_write: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None) = None) → [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]

Given a set of file mode bits ([`st_mode`](https://docs.python.org/3/library/os.html#os.stat_result.st_mode)), this function suggests new permissions
from a small set of “simple” permissions (0o444, 0o555, 0o644, 0o755, 0o664, 0o775).

* **Parameters:**
  * **st_mode** – The original mode bits *including* the file type information.
    Usually, you would take this from [`os.stat_result.st_mode`](https://docs.python.org/3/library/os.html#os.stat_result.st_mode) as returned by [`os.lstat()`](https://docs.python.org/3/library/os.html#os.lstat) or [`pathlib.Path.lstat()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.lstat).
  * **group_write** – 

    Whether the suggestion should have the group write bit set.
    Note that the group write bit is *never* suggested unless the original has the user write bit set.
    - When [`None`](https://docs.python.org/3/library/constants.html#None) (the default), the suggestion is based on the original group write bit.
    - When [`False`](https://docs.python.org/3/library/constants.html#False), the suggestion never has the group write bit set.
    - When [`True`](https://docs.python.org/3/library/constants.html#True), the suggestion always has the group write bit set.
* **Returns:**
  A tuple consisting of the file’s original permissions and suggested permissions to use instead,
  based on the arguments to this function, the file’s original user permission bits, and whether it is a directory or not.
  The two values may be equal indicating that no change is suggested. No changes are ever suggested for symbolic links.

## Author, Copyright, and License

Copyright (c) 2022-2024 Hauke Dämpfling ([haukex@zero-g.net](mailto:haukex@zero-g.net))
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, [https://www.igb-berlin.de/](https://www.igb-berlin.de/)

This library is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)
