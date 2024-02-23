#!/usr/bin/env python3

import argparse
import sys
import typing as t
from pathlib import Path

import yaml

# TYPES of Data as Read from Yaml Config

## job names are yaml keys
JobName = t.NewType('JobName', str)

## each job 'needs' key can be:
#   - missing -> python None
#   - a string value expected to be a job name -> python JobName
#   - a list value, with jobs names as items -> python List[JobName]

# OPT 2
# Define a new type for JobNeeds
# JobNeedsType = t.Union[JobName, t.List[JobName], None]
# JobNeeds = t.NewType('JobNeeds', JobNeedsType)
# # OPT 1
JobNeeds = t.Union[JobName, t.List[JobName], None]


ParsedYaml = t.Dict[str, t.Any]

# TYPES of Data Model
JobsNeedsValue = t.List[JobName]


# Parse the GitHub Actions YAML file
def parse_actions_config(filename: t.Union[str, Path]) -> t.Union[ParsedYaml, None]:
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None


# Extract job names and their 'needs' sections
def extract_job_dependencies(config: ParsedYaml) -> t.Dict[str, JobsNeedsValue]:
    """Understand DAG of all Jobs"""
    # DAG representation

    # mapping of job names to their dependencies (previous steps in the dependency DAG)
    job_dependencies: t.Dict[str, JobsNeedsValue] = {}

    if 'jobs' not in config:
        print("[WARNGING] No 'jobs' section found in config file")

    else:
        for job_name, job_config in config['jobs'].items():
            needs: JobNeeds = job_config.get('needs')

            current_job_needs_value: JobsNeedsValue = []
            if isinstance(needs, str):  # single dependency
                current_job_needs_value = [needs]
            elif isinstance(needs, list):  # multiple dependencies
                current_job_needs_value = needs
            elif needs is not None:
                print(f"[WARNING] Unexpected 'needs' value: {needs}")

            job_dependencies[job_name] = current_job_needs_value

    return job_dependencies


# Generate Mermaid markdown from job dependencies
def generate_mermaid(job_dependencies: t.Dict[str, t.List[str]]) -> str:
    mermaid_code = 'graph LR;\n'
    for job_name, needs in job_dependencies.items():
        for need in needs:
            mermaid_code += f'  {need} --> {job_name}\n'
    return mermaid_code


def mermaid_from_yaml(filename: t.Union[str, Path], format: str = 'md') -> str:
    config: ParsedYaml = parse_actions_config(filename)
    if config is None:
        print(f"[ERROR] Could not parse YAML file: {filename}")
        sys.exit(1)
    job_dependencies: t.Dict[str, JobsNeedsValue] = extract_job_dependencies(config)
    mermaid_code: str = generate_mermaid(job_dependencies)

    TAB = 3 * ' '

    ## Embed Mermaid to MARKDOWN ##
    if format == 'md':
        embeded_mermaid: str = (
            # "## CI/CD Pipeline\n\n"
            # f"**CI Config File: {filename}**\n\n"
            f"```mermaid\n{mermaid_code}```\n"
        )
    ## Embed Mermaid to RST ##
    elif format == 'rst':
        embeded_mermaid: str = ".. mermaid::\n\n" + '\n'.join(
            [TAB + x for x in mermaid_code.split('\n')]
        )
    return embeded_mermaid


#### MAIN ####
def main():
    args = arg_parse()

    if args.input == "default-path":
        ci_config = Path.cwd() / ".github/workflows/test.yaml"
        # ci_config_file = Path(__file__).parent / "ci-config.yml"
        # input_data = sys.stdin.read()
    else:
        ci_config = Path(args.input)

    md: str = mermaid_from_yaml(ci_config, format='rst' if args.rst else 'md')

    if args.output:
        # Handle the case of writing to an output file
        output_file = Path(args.output)
        output_file.write_text(md)
    else:
        # Handle the case of streaming output to stdout
        sys.stdout.write(md)
        # print


# CLI
def arg_parse():
    parser = argparse.ArgumentParser(
        description="Command-line tool to handle input and output options."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="default-path",
        help="Input file path (default: 'default-path')",
    )
    parser.add_argument(
        '--rst',
        help='Whether to generate RST content. Default MD',
        action='store_true',
        default=False,
    )
    parser.add_argument("-o", "--output", help="Output file path")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
