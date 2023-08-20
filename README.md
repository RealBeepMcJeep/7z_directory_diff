used for creating "patch" 7z files by detecting differences between an existing 7z file(s) and the current state of a target directory.

uses txt dumps from the `7z l -slt` command

eg of usage:
run in directory with the 7z files
```bash
7z l -slt first_backup.7z > first_backup.7z.txt
7z l -slt diff_1.7z > diff_1.7z.txt
7z l -slt diff_2.7z > diff_2.7z.txt
```
- move txt files produced to directory immediately above target backup directory (important relative paths are conserved and consistent).
- also move main.py to directory immediately above target backup directory (important relative paths are conserved and consistent).
- change constants in main.py.
```py
_7Z_DUMP_FILES = ['first_backup.7z.txt', 'diff_1.7z.txt', 'diff_2.7z.txt']
DIR_TO_DIFF = 'app_directory'
```

should spit out what paths contain files that are different from anything in first_backup.7z layered over by diff_1.7z layered over by diff_2.7z. using this information we can build a diff_3.7z.
