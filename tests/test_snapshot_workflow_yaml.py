"""Validate generated Github Workflows for logical errors"""

import typing as t
from pathlib import Path

import pytest


# @pytest.fixture(params=["gold-standard", "biskotaki-no-input", "biskotaki-interactive"])
# def snapshot_project_data(request, test_root: Path) -> Path:
#     return test_root / 'data' / 'snapshots' / request.param, request.param


@pytest.mark.parametrize(
    'snapshot',
    ["biskotaki-gold-standard", "biskotaki-no-input", "biskotaki-interactive"],
)
def test_referenced_job_output_vars_correspond_to_existing_jobs(
    # GIVEN a Snapshot from calling the Generator
    # snapshot_project_data: t.Tuple[Path, str],
    snapshot: str,
    test_root: Path,
):
    """Test that for a given snapshot project, its source Github Action workflows
    yaml files "correctly" reference other jobs' output variables.

    This is a regression test to ensure that the generated workflows are
    logically correct and do not reference non-existing jobs.
    """
    SNAPSHOT_PROJECT = test_root / 'data' / 'snapshots' / snapshot
    SNAPSHOT_NAME = snapshot

    CICDDesignOption = t.Literal["stable", "experimental"]

    # GIVEN the supported 'cicd' options, available in 'generate-python' CLI
    CICD_OPTIONS: t.Set[CICDDesignOption] = {"stable", "experimental"}

    # GIVEN the EXPECTED paths to the generated Github Workflows per CICD Option
    from cookiecutter_python.hooks.post_gen_project import CICD_DELETE

    all_rendered_yaml_workflows: t.Set[t.Tuple[str, ...]] = {
        tuple_of_strings
        for list_of_tuples in CICD_DELETE.values()
        for tuple_of_strings in list_of_tuples
    }

    # Sanity check that the generated workflows are not empty, otherwise the test is pointless
    assert all_rendered_yaml_workflows, "No generated workflows found!"
    assert all(
        [type(x) is tuple for x in all_rendered_yaml_workflows]
    ), "All paths should be tuples of strings"

    cicd_option_2_yaml_file_paths: t.Dict[CICDDesignOption, t.Iterable[Path]] = {
        # "stable": [test_root / '.github' / 'workflows' / 'test.yaml'],
        # "experimental": [test_root / '.github' / 'workflows' / 'cicd.yml'],
        cicd_option: [
            SNAPSHOT_PROJECT / Path(*workflow_path_tuple)
            for workflow_path_tuple in all_rendered_yaml_workflows
            if workflow_path_tuple not in set(CICD_DELETE[cicd_option])
        ]
        for cicd_option in CICD_OPTIONS
    }
    # assert cicd_option_2_yaml_file_paths == {}
    assert cicd_option_2_yaml_file_paths and all(
        cicd_option_2_yaml_file_paths.values()
    ), "No workflows found!"
    assert all(
        [type(x) is list for x in cicd_option_2_yaml_file_paths.values()]
    ), "All values should be lists of paths"

    # GIVEN we maintain a registry of the cicd options used at generation time for every Snapshot
    snapshot_name_2_cicd_option_value: t.Dict[str, CICDDesignOption] = {
        'biskotaki-gold-standard': 'experimental',
        # BISKOTAKI CI (user config yaml)
        'biskotaki-no-input': 'experimental',
        'biskotaki-interactive': 'experimental',
    }
    # GIVEN we identify the Snapshot's project cicd option used at generation time
    snapshot_cicd_value: CICDDesignOption = snapshot_name_2_cicd_option_value[SNAPSHOT_NAME]

    # WHEN we iterate over the expected generated workflows for this Snapshot
    import yaml

    for yaml_workflow in cicd_option_2_yaml_file_paths[snapshot_cicd_value]:
        with yaml_workflow.open() as f:
            # GIVEN we successfully load the yaml file
            yaml_dict = yaml.safe_load(f)

            # GIVEN all the declared jobs in the workflow
            jobs: t.Dict[str, t.Dict[str, t.Any]] = yaml_dict["jobs"]

            # TODO: "scan" all job key/value pairs and not only those in the 'with' dict

            for job_name, job_data in (
                (job_name, job_data)
                for job_name, job_data in jobs.items()
                if 'with' in job_data
            ):
                # we start small: only verify on jobs that call other reusable workflows
                with_dict = job_data['with']

                # here every key maps to a reusable workflow input value

                # we try to find patterns such as '${{ needs.test_suite.outputs.PEP_VERSION }}'
                for value in (
                    value
                    for value in with_dict.values()
                    if isinstance(value, str) and 'needs.' in value
                ):
                    # WHEN we scan all values passed to the reusable workflow
                    parts = value.split('needs.')
                    job_name_referenced: str = parts[1].split('.')[0]
                    # AND verify that job_name_referenced is in the jobs
                    assert (
                        job_name_referenced in jobs
                    ), f"Job {job_name} references variables from other jobs, but {job_name_referenced} is not a job."

    # THEN we have successfully verified that all jobs that reference variables from other jobs also depend on those jobs
    # and the test passes
