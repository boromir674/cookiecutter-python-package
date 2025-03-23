import typing as t
from pathlib import Path


def test_dialog_prompts_for_all_cookiecutter_variables(get_object, distro_loc):
    """Test Interactive Mode, prompts for all Cookiecutter Variables.

    Verifies that when User runs Generator in Interactive Mode, they will be
    prompted for all Cookiecutter Variables.

    If any Cookiecutter Variable is not prompted for, the test will fail.
    """

    # GIVEN the Cookiecutter Variables
    cookie_json_file: Path = distro_loc / "cookiecutter.json"
    assert cookie_json_file.exists(), f"File Not Found: {cookie_json_file}"
    assert cookie_json_file.is_file(), f"Not a File: {cookie_json_file}"
    import json

    _cookie_vars: t.Iterable[str] = json.loads(cookie_json_file.read_text()).keys()

    # GIVEN how the Interactive Dialogs produce the Context Variable Values
    from cookiecutter_python.backend.pre_main import pre_main
    from cookiecutter_python.backend.request import Request

    # WHEN Context is created in Interactive Mode
    def emulated_prompt(questionary_data: t.List[t.Mapping[str, t.Any]]):
        """Emulate the Dialog Prompt, and return the Context."""
        # THEN Context contains all Cookiecutter Variables
        assert {x['name'] for x in questionary_data} == (
            set(_cookie_vars) - {'interpreters'}
        ).union(set(['supported-interpreters'])), (
            f"Missing: from {_cookie_vars}.\n"
            "Dialog Prompts must be kept in sync with Cookiecutter Variables!\n\n"
            "If missing variables from Dialog Prompts, this means that cookiecutter.json\n"
            "got added new Variables, and the Dialogs need to be updated, to stay in sync.\n\n"
            "Make sure Variables in src/cookiecutter_python/cookiecutter.json all have a"
            "corresponding element (name), found in the dialog list passed in the prompt"
            "of src/cookiecutter_python/handle/dialogs/lib/project_name.py and in"
            "the src/cookiecutter_python/backend/helpers.py client code.\n\n"
        )
        return {'supported-interpreters': []}

    # Dynamic Import of dialogs.lib.project_name module and MonkeyPatch prompt
    get_object(
        'prompt',
        'cookiecutter_python.handle.dialogs.lib.project_name',
        overrides={'prompt': lambda: emulated_prompt},
    )

    context_res = pre_main(
        Request(
            config_file=None,
            default_config=False,
            web_servers=['pypi', 'readthedocs'],
            no_input=False,
            extra_context=None,
        )
    )

    runtime_content = context_res.extra_context
    assert runtime_content == {
        'interpreters': {'supported-interpreters': []}
    }, "Emulated function removed, but assertion was not updated. Update this line or emulated function to fix test logic."
