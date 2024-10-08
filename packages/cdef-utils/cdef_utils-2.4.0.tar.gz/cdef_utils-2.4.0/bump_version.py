import os
import re
import shutil
import subprocess


def bump_version(version, part="patch"):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_file(file_path, pattern, replacement):
    with open(file_path, "r") as file:
        content = file.read()

    updated_content = re.sub(pattern, replacement, content)

    with open(file_path, "w") as file:
        file.write(updated_content)


def clear_cache(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Cleared cache: {directory}")


def remove_dist_files(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Removed distribution files: {directory}")


def main(part="patch"):
    # Get the current version from pyproject.toml
    with open("cdef-utils/pyproject.toml", "r") as file:
        content = file.read()
        match = re.search(r'version = "(.*?)"', content)
        if match:
            current_version = match.group(1)
        else:
            raise ValueError("Version not found in pyproject.toml")

    new_version = bump_version(current_version, part)
    print(f"Bumping version from {current_version} to {new_version}")

    # Update pyproject.toml
    update_file(
        "cdef-utils/pyproject.toml", r'version = ".*?"', f'version = "{new_version}"'
    )

    # Update pixi.toml
    update_file(
        "cdef-utils/pixi.toml", r'version = ".*?"', f'version = "{new_version}"'
    )

    # Clear caches
    clear_cache("cdef-utils/.pytest_cache")
    clear_cache("cdef-utils/.ruff_cache")

    # Remove distribution files
    remove_dist_files("cdef-utils/dist")

    # Run the build task
    subprocess.run(["pixi", "run", "build"], cwd="cdef-utils", check=True)

    print(f"Version bumped to {new_version} and build completed successfully.")


if __name__ == "__main__":
    import sys

    part = sys.argv[1] if len(sys.argv) > 1 else "patch"
    main(part)
