#!/usr/bin/env python

import os
import sys
import configparser
import re


MY_DIR = os.path.dirname(os.path.realpath(__file__))


def read_config_file(file_path: str):
    config = configparser.ConfigParser()
    config.read(file_path)
    d = {'install_requires': lambda _config: _config['options']['install_requires']}
    return type("Sections", (), {
        'get': lambda name: d.get(name, lambda _config: _config['options.extras_require'][name])(config)
    })


def parse_requirements(string):
    package_name_pattern = '\w[\w_\-\d]*'
    operator_pattern = '(?:==|>=|<=|~=|=<|=>)'
    
    version_pattern = '(?:[1-9]\d+|[0-9])(?:\.(?:[0-9]\d+|[0-9]))*(?:-(?:P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?:P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'
    requirement_pattern = '({package})\s*({operator})\s*({version})'.format(
        package=package_name_pattern,
        operator=operator_pattern,
        version=version_pattern,
    )
    return re.compile(requirement_pattern).findall(string)


def generate(sections, section_names):
    for section_name in section_names:
        yield sections.get(section_name)


def get_requirements(section_names, sections):
    return [parse_requirements(section_string) for section_string in generate(sections, section_names)]


def format_section_output(requirements):
    return '\n'.join((
        '{package} {operator} {version}'.format(
            package=requirement_data[0],
            operator=requirement_data[1],
            version=requirement_data[2],
        ) for requirement_data in requirements
    ))


def main(*args, **kwargs):
    sections = args[0]
    if not sections:
        print('no sections')
        sys.exit(1)

    project_root = kwargs.get('project_root', MY_DIR)
    config_file = os.path.join(project_root, '..', 'setup.cfg')

    existing_sections = read_config_file(config_file)

    requirements = get_requirements(sections, existing_sections)
    result = '\n\n'.join((
        format_section_output(section_requirements) for section_requirements in requirements
    ))
    return result


if __name__ == '__main__':
    res = main(sys.argv[1:])
    print(res)
