from typing import Any, MutableMapping, Optional, Union
from pathlib import Path


def get_user_config(
    config_file: Optional[str], default_dict: Optional[bool]
) -> MutableMapping[str, Any]: ...


def get_config(config_path: Union[str, Path]) -> MutableMapping[str, Any]: ...
