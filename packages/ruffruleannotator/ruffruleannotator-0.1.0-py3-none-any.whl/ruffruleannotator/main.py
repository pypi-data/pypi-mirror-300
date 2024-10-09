import argparse
from pathlib import Path

from .ruffruleannotator import annotate

CONFIG_FILES = ["pyproject-test.toml", "pyproject.toml", "ruff.toml"]

CRED = "\33[31m"
CGREEN = "\33[32m"
CEND = "\033[0m"


def create_backup(fname):
    import shutil

    project_dir = Path.cwd()
    backup_dir = (
        Path.home() / ".ruffruleannotator" / "backup" / project_dir.relative_to("/")
    )

    backup_dir.mkdir(exist_ok=True, parents=True)

    backup_file = backup_dir / fname

    print(backup_file)

    shutil.copy2(fname, backup_file)

    return backup_file


def compute_diff(config, formatted_config):
    from difflib import unified_diff

    diff = list(unified_diff(config, formatted_config, lineterm=""))

    for i, line in enumerate(diff):
        if line.startswith("+"):
            diff[i] = CGREEN + line + CEND
        if line.startswith("-"):
            diff[i] = CRED + line + CEND

    return "\n".join(list(diff))


def execute(
    backup: bool = True,
    sort_lines: bool = True,
    verify_changes: bool = False,
    dry: bool = False,
):
    for fname in CONFIG_FILES:
        if not Path(fname).exists():
            continue

        with open(fname) as f:
            config = f.read()

        if fname != "ruff.toml" and "[tool.ruff" not in config:
            continue

        print(f"Found ruff config in '{fname}'")

        config = config.splitlines()
        formatted_config = annotate(config, sort_lines)

        if config == formatted_config:
            print("No changes to apply")
            exit(0)

        diff = compute_diff(config, formatted_config)
        print("\n" + diff + "\n")

        if dry:
            print("Dry run - changes not applied")
            exit(0)

        if verify_changes:
            input("Press enter to apply changes")

        if backup:
            backup_file = create_backup(fname)
            print(f"Stored backup here: '{backup_file}'")

        with open(fname, "w") as f:
            f.write("\n".join(formatted_config))
            print("Reformatted config")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--no-backup",
        dest="no_backup",
        action="store_true",
        help="Skip creation of config backup",
    )
    parser.add_argument(
        "--no-sort",
        dest="no_sort",
        action="store_true",
        help="Keep order of rules unchanged",
    )
    parser.add_argument("--yes", action="store_true", help="Skip user confirmation")
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Do not apply changes to file",
    )

    args = parser.parse_args()

    try:
        execute(
            backup=not args.no_backup,
            sort_lines=not args.no_sort,
            verify_changes=not args.yes,
            dry=args.dry,
        )
    except KeyboardInterrupt:
        exit(0)
