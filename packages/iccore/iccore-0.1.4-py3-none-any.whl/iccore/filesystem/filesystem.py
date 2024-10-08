"""
This module has wrappers over Python built-ins for filsystem operations
"""

import shutil
from pathlib import Path
import os

from iccore.runtime import ctx


def copy(src: Path, dst: Path) -> None:
    """
    Copy the file or directory from `src` to `dst`
    :param src: The location to copy from
    :param dst: The location to copy to
    """

    if ctx.can_modify():
        shutil.copy(src, dst)
    else:
        ctx.add_cmd(f"copy {src} {dst}")


def make_archive(archive_name: Path, fmt: str, src: Path) -> None:
    """
    Create an archive with name `archive_name` and chosen format, e.g. zip
    from the content in `src`
    :param archive_name: The path to the created archive
    :param fmt: The desired archive format, e.g. zip
    :param src: The src of the content to be archived
    """

    if ctx.can_modify():
        shutil.make_archive(str(archive_name), fmt, src)
    else:
        ctx.add_cmd(f"make_archive {archive_name} {fmt} {src}")


def unpack_archive(src: Path, dst: Path) -> None:
    """
    Extract the archive at `src` to `dst`
    """

    if ctx.can_modify():
        shutil.unpack_archive(src, dst)
    else:
        ctx.add_cmd(f"unpack_archive {src} {dst}")


def copy_files(src: Path, dst: Path):
    """
    Copy all files from the `src` directory
    to the `dst` directory
    """
    for direntry in src.iterdir():
        if direntry.is_file():
            shutil.copy(direntry, dst)


def copy_files_relative(paths: list[Path], src: Path, dst: Path):
    """
    For each relative path in `paths` copy the file at `src/path` to
    `dst/path`
    """

    for path in paths:
        shutil.copy(src / path, dst / path)


def clear_dir(src: Path):
    """
    If there is a directory at `src` delete it and make a new one
    """

    if src.exists():
        shutil.rmtree(src)
    os.makedirs(src)


def read_file(src: Path):
    with open(src, "r", encoding="utf-8") as f:
        return f.read()


def read_file_lines(src: Path):

    with open(src, "r", encoding="utf-8") as f:
        return f.readlines()


def write_file_lines(
    src: Path, lines: list[str], make_parents: bool = True, make_exe: bool = False
):

    if make_parents:
        os.makedirs(src.parent, exist_ok=True)

    with open(src, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)

    if make_exe:
        os.chmod(src, 0o0755)


def write_file(src: Path, content: str, make_parents: bool = True):
    if make_parents:
        os.makedirs(src.parent, exist_ok=True)

    with open(src, "w", encoding="utf-8") as f:
        f.write(content)


def replace_in_file(src: Path, search_term: str, replace_term: str) -> bool:

    content = read_file_lines(src)
    has_update = False
    for idx, line in enumerate(content):
        replaced_line = line.replace(search_term, replace_term)
        if replaced_line != line:
            content[idx] = replaced_line
            has_update = True
    if has_update:
        write_file_lines(src, content)
        return True
    return False


def replace_in_files(
    src: Path, search_term: str, replace_term: str, extension: str
) -> int:

    count = 0
    for direntry in src.iterdir():
        if direntry.is_file():
            if not extension or direntry.suffix == f".{extension}":
                replaced = replace_in_file(direntry, search_term, replace_term)
                if replaced:
                    count += 1
    return count


def file_contains_string(src: Path, search_term: str) -> bool:
    content = read_file(src)
    return search_term in content


def get_dirs(path: Path, prefix: str = "") -> list[Path]:
    if prefix:
        return [
            entry
            for entry in path.iterdir()
            if entry.is_dir() and entry.name.startswith("task_")
        ]
    return [entry for entry in path.iterdir() if entry.is_dir()]
