#!/usr/bin/env python
import argparse
import re
import sys
import typing as t
from pathlib import Path


def parse_dockerfile(dockerfile_path):
    # Stages built from 'FROM <a> AS <b> statements
    stages = {}
    # copies built from 'COPY --from=<a> <source_path> <target_path>' statements
    copies = {}
    # Line match at current line
    stage_alias = None
    stage_name_reg = r'[\w:\.\-_]+'
    stage_reg = re.compile(
        rf'^FROM\s+(?P<stage>{stage_name_reg})\s+[Aa][Ss]\s+(?P<alias>{stage_name_reg})'
    )

    copy_from_reg = re.compile(
        rf'^COPY\s+\-\-from=(?P<prev_stage>{stage_name_reg})\s+'
        + r'(?P<path>[\w\.\-:/_\${}]+)\s+'
    )
    # Algo:
    #  go line by line
    #  check if line is a stage
    #  if so, add it to the stages dict
    #  check if line is a copy
    #  if so, add it to the copies dict
    with open(dockerfile_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()

            # Check if it's a new stage
            # each stage has a unique alias in the Dockerfile
            stage_match = stage_reg.match(line)
            if stage_match:  # FROM <a> AS <b>
                stage_alias = stage_match.group('alias')  # <b>

                # we create an empty list for pointing to "prev" stages
                stages[stage_alias] = []
                copies[stage_alias] = []
                from_stage = stage_match.group('stage')  # <a>
                # Add instructions to current stage
                if stage_alias:  # use FROM <a> AS <b>, to store a as previous to b
                    stages[stage_alias].append(from_stage)
            elif match := copy_from_reg.match(
                line
            ):  # COPY --from=<a> <source_path> <target_path>
                copied_from_stage: str = match.group('prev_stage')
                path_copied: str = match.group('path')
                copies[stage_alias].append((copied_from_stage, path_copied))

    return stages, copies


def generate_mermaid_flow_chart(dockerfile_dag):
    stages: t.Dict[str, t.List[str]] = dockerfile_dag[0]
    thick_line_with_arrow = '-->'
    copies: t.Dick[str, t.List[t.Tuple[str, str]]] = dockerfile_dag[1]
    dotted_arrow_with_text = '-. "{text}" .->'

    chart = "graph TB;\n"

    # Each stage maps to a list of previous FROM stages
    # and a list of previous 'COPY --from' stages

    for stage, prev_stages in stages.items():
        # Connect 'FROM <a> AS <b>' Stages
        for prev_stage in prev_stages:
            chart += f"  {prev_stage} {thick_line_with_arrow} {stage}\n"

        # Connect 'COPY --from<a> <path> <dest>' statements
        prev_copies = copies.get(stage, [])
        for prev_copy in prev_copies:
            prev_stage: str = prev_copy[0]
            # write copied path in arrow text
            path_copied: str = prev_copy[1]
            chart += (
                f"  {prev_stage} "
                + dotted_arrow_with_text.format(text=path_copied)
                + f" {stage}\n"
            )

    return chart


## Embed Mermaid to MARKDOWN ##
def generate_markdown(dockerfile_dag, flavor='normal'):
    flow_chart = generate_mermaid_flow_chart(dockerfile_dag)

    bar_symbol = '`'
    if flavor == 'az':  # in az the ':' is needed by markdown processor
        bar_symbol = ':'

    markdown = (
        "## Dockerfile Flow Chart\n\n"
        f"**Dockerfile: {dockerfile_path}**\n\n"
        f"{bar_symbol * 3}mermaid\n{flow_chart}{bar_symbol * 3}\n"
    )
    return markdown


## Embed Mermaid to RST ##
def generate_rst(dockerfile_dag, **kwargs):
    flow_chart = generate_mermaid_flow_chart(dockerfile_dag)

    TAB = 3 * ' '
    # "Dockerfile Flow Chart\n"
    # f"====================\n\n"
    # f"Dockerfile: {dockerfile_path}\n\n"
    rst = ".. mermaid::\n\n" + '\n'.join([TAB + x for x in flow_chart.split('\n')])
    return rst


def parse_cli_args() -> t.Tuple[Path, t.Optional[str]]:
    parser = argparse.ArgumentParser(description='Process Dockerfile paths.')

    parser.add_argument(
        'dockerfile_path',
        nargs='?',
        default='Dockerfile',
        help='Path to the Dockerfile',
    )
    parser.add_argument(
        '-o', '--output', help='Output path. If not specified, print to stdout.'
    )
    parser.add_argument(
        '--rst',
        help='Whether to generate RST content. Default MD',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--md-flavour',
        help='Whether to tailor for markdown for "exotic" azure devops markdown processor (defaults to no). Only applies is --rst flag is not passed',
        action='store_true',
        default=False,
        # custom var name to store variable
        dest='az',
    )
    args = parser.parse_args()

    dockerfile: Path = Path(args.dockerfile_path)
    if not dockerfile.exists():
        # explicitly use cwd to try again to find it
        dockerfile = Path.cwd() / args.dockerfile_path

    return dockerfile, args


def parse_dockerfile_handler(
    dockerfile_parser: t.Callable[[str], str], dockerfile_path: str
) -> t.Optional[str]:
    try:
        return dockerfile_parser(dockerfile_path)
    except AttributeError as error:
        print(
            "[ERROR] Error parsing Dockerfile\n"
            f"[Exception] {error}\n"
            "Most probably the Dockefile has a syntax error!\n"
            "Or either the regex is wrong, but it unlikely.\n"
            "Interupting and exiting...\n"
        )
    except FileNotFoundError as error:
        print(
            "[ERROR] Error parsing Dockerfile\n"
            f"[Exception] {error}\n"
            "Most probably the Dockerfile does not exist!\n"
            "Interupting and exiting...\n"
        )


if __name__ == '__main__':
    # Data
    dockerfile_path, args = parse_cli_args()
    output_path = args.output
    docs_format = {True: generate_rst, False: generate_markdown}

    dockerfile_dag = parse_dockerfile_handler(parse_dockerfile, dockerfile_path)
    if dockerfile_dag is None:
        sys.exit(1)

    content: str = docs_format[args.rst](
        dockerfile_dag, flavour='normal' if not args.az else 'az'
    )
    if output_path is None:
        print(content)
        sys.exit(0)

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"{'RST' if args.rst else 'MARKDOWN'} generated and saved to {output_path}")
    sys.exit(0)
