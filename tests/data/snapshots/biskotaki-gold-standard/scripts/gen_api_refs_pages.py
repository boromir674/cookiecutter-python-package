"""Generate the code reference pages."""

import typing as t
from pathlib import Path

import mkdocs_gen_files

# Initialize the navigation object
nav = mkdocs_gen_files.Nav()

# Search inside 'src' dir for python 'packages' (dirs with __init__.py)
src = Path(__file__).parent.parent / "src"

cli_module_path: t.Optional[Path] = None


# Loop, recursively, over all Python *.py Files, inside 'src' dir and subdirs
for path in sorted(src.rglob("*.py")):
    ## 1. extract Relative path from Python File and remove suffix (.py)
    # EG src/biskotaki/cli.py  -->   biskotaki/cli
    _module_path = path.relative_to(src).with_suffix("")
    ## 2. derive corresponding Docs File to write Directives into
    # EG biskotaki/cli  -->   biskotaki/cli.md
    doc_path = path.relative_to(src).with_suffix(".md")
    ## 3. derive Full Path to Docs File
    full_doc_path = Path("reference", doc_path)

    parts = list(_module_path.parts)

    # Skip __main__ Files
    if parts[-1] == "__main__":
        continue

    # For __init__ Files dedicate an index.md file, instead of __init__.md
    if parts[-1] == "__init__":
        parts = parts[:-1]
        ## https://mkdocstrings.github.io/recipes/#bind-pages-to-sections-themselves
        doc_path = doc_path.with_name("index.md")
        # full_doc_path = full_doc_path.with_name("index.md")

    if parts[-1] == 'cli':
        cli_module_path = _module_path

    ## Progressively build the navigation object, creating a mapping:
    # Navigatiion Item --> Docs File Path, *.md, with content for mkdocs build
    # Sequence[str] --> str
    nav[parts] = doc_path.as_posix()
    # nav[parts] = str(doc_path)  # use this in case as_posix() fails on windows

    # Write Contents for Item, with some kind of directive
    with mkdocs_gen_files.open(Path("reference", doc_path), "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

# Dedicate a custom Page for Entrypoint CLI, apart from auto-generated
# Automatic discovery happens, if a top-level cli.py file is found.
if cli_module_path:
    # we want to place CLI in top-level navigation
    navigation_key: t.Sequence[str] = ["CLI"]
    # arbitrary Docs file name, since we will inject its contents automatically
    doc_path = Path("CLI.md")

    # Add to Navigation Item
    nav[navigation_key] = doc_path.as_posix()

    # Top-Level CLI.md Docs Contents: mainly using the 'mkdocs-click' Directive
    CLI_DOC_CONTENT = """
# CLI Reference

This page provides documentation for our command line tools.

::: mkdocs-click
    :module: biskotakigold.cli
    :command: main
"""
    # TODO: write better content for the CLI.md file
    with mkdocs_gen_files.open(Path("reference", doc_path), "w") as fd:
        fd.write(CLI_DOC_CONTENT)

    # ROOT
    #  -> docs
    #     -> scripts
    # -> src/python_package
    mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)
    # so that it correctly sets the edit path of (for example) nst_math.py to
    # <repo_url>/blob/master/src/artificial_artwork/nst_math.py instead of
    # <repo_url>/blob/master/docs/src/artificial_artwork/nst_math.py

    # mkdocs_gen_files.set_edit_path(full_doc_path, path)


# At the end, create a magic, literate navigation file called SUMMARY.md in the
# reference folder.
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    # Write the navigation as a Markdown list in the literate navigation file
    nav_file.writelines(nav.build_literate_nav())

# Now we are able to remove our hard-coded navigation in mkdocs.yml,
# and replace it with a single line!

# IE: - Code Reference: reference/
# Note the trailing slash! It is needed so that mkdocs-literate-nav knows it has
# to look for a SUMMARY.md file in that folder
