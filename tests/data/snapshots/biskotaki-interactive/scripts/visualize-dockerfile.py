#!/usr/bin/env python
import argparse
import re
import typing as t
from pathlib import Path


def parse_dockerfile(dockerfile_path):
    # Stages built from 'FROM <a> AS <b> statements
    stages = {}
    # copies built from 'COPY --from=<a> <source_path> <target_path>' statements
    copies = {}
    # Line match at current line
    current_stage = None
    stage_name_reg = r'[\w:\.\-]+'
    stage_reg = re.compile(
        rf'^FROM\s+(?P<stage>{stage_name_reg})\s+[Aa][Ss]\s+(?P<alias>{stage_name_reg})'
    )

    copy_from_reg = re.compile(
        r'^COPY\s+\-\-from=(?P<prev_stage>[\w\.\-:]+)\s+(?P<path>[\w\.\-:/]+)'
    )

    with open(dockerfile_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()

            # Check if it's a new stage
            # each stage has a unique alias in the Dockerfile
            stage_match = stage_reg.match(line)
            if stage_match:  # FROM <a> AS <b>
                current_stage = stage_match.group('alias')

                # we create an empty list for pointing to "prev" stages
                stages[current_stage] = []
                copies[current_stage] = []
                try:
                    previous_stage = stage_match.group('stage')
                except AttributeError as error:
                    print(f'[DEBUG] Line: {line}')
                    print(f"Error: {error}")
                    raise error
                # Add instructions to current stage
                if current_stage:
                    stages[current_stage].append(previous_stage)
            else:
                match = copy_from_reg.match(line)
                if match:  # COPY --from=<a> <source_path> <target_path>
                    previous_stage: str = match.group('prev_stage')
                    path_copied: str = match.group('path')
                    copies[current_stage].append((previous_stage, path_copied))

    return stages, copies


def generate_mermaid_flow_chart(dockerfile_dag):
    stages: t.Dict[str, t.List[str]] = dockerfile_dag[0]
    thick_line_with_arrow = '-->'
    copies: t.Dick[str, t.List[t.Tuple[str, str]]] = dockerfile_dag[1]
    dotted_arrow_with_text = '-. "{text}" .->'

    chart = "graph TB;\n"

    for stage, prev_stages in stages.items():
        # chart += f"  {stage}({stage})\n"

        # Connect 'FROM <a> AS <b>' Stages
        for prev_stage in prev_stages:
            chart += f"  {prev_stage} {thick_line_with_arrow} {stage}\n"

        # Connect 'COPY --from<a> <path> <dest>' statements
        prev_copies = copies.get(stage, [])
        for prev_copy in prev_copies:
            prev_stage: str = prev_copy[0]
            # write copied path in arrow text
            # path_copied: str = prev_copy[1]
            # chart += f"  {prev_stage} " + dotted_arrow_with_text.format(text=path_copied) + f" {stage}\n"
            # write COPY (literal) in arrow text
            chart += (
                f"  {prev_stage} " + dotted_arrow_with_text.format(text='COPY') + f" {stage}\n"
            )

    return chart


def generate_markdown(dockerfile_path, output_path):
    dockerfile_dag = parse_dockerfile(dockerfile_path)

    flow_chart = generate_mermaid_flow_chart(dockerfile_dag)

    markdown = (
        "## Dockerfile Flow Chart\n\n"
        f"**Dockerfile: {dockerfile_path}**\n\n"
        f"```mermaid\n{flow_chart}```\n"
    )
    if output_path is None:
        print(markdown)
        return
    with open(output_path, 'w') as f:
        f.write(markdown)

    print(f"Markdown generated and saved to {output_path}")


def parse_cli_args() -> t.Tuple[Path, t.Optional[str]]:
    parser = argparse.ArgumentParser(description='Process Dockerfile paths.')

    parser.add_argument(
        'dockerfile_path', nargs='?', default='Dockerfile', help='Path to the Dockerfile'
    )
    parser.add_argument(
        '-o', '--output', help='Output path. If not specified, print to stdout.'
    )

    args = parser.parse_args()

    dockerfile: Path = Path(args.dockerfile_path)
    if not dockerfile.exists():
        # explicitly use cwd to try again to find it
        dockerfile = Path.cwd() / args.dockerfile_path

    return dockerfile, args.output


if __name__ == '__main__':
    dockerfile_path, output_path = parse_cli_args()
    generate_markdown(dockerfile_path, output_path)
