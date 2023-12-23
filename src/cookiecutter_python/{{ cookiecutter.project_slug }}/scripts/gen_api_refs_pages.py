"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent / "src"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        ## https://mkdocstrings.github.io/recipes/#bind-pages-to-sections-themselves
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
        ##
    elif parts[-1] == "__main__":
        continue

    # Progressively build the navigation object
    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

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
