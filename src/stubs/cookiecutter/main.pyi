from typing import Optional

def cookiecutter(
    template: str,
    checkout: Optional[str],
    no_input: bool,
    extra_context: Optional[dict],
    replay: bool,
    overwrite_if_exists: bool,
    output_dir: Optional[str],
    config_file: Optional[str],
    default_config: bool,
    password: Optional[str],
    directory: Optional[str],
    skip_if_file_exists: bool,
) -> str: ...
