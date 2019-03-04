#!/usr/bin/env python

import sys

from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.constructor import Constructor

# Don't convert string "true" and "false" to python True/False
def add_bool(self, node):
    return self.construct_scalar(node)

Constructor.add_constructor(u'tag:yaml.org,2002:bool', add_bool)


def render_template(template, input_yaml_file):

    try:
        f = open(input_yaml_file, 'r')
        f.close()
    except IOError:
       print(f'unable to open {input_yaml_file} file')
       sys.exit(1)

    with open(input_yaml_file, 'r') as stream:
        try:
            vpcs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

        msg = template.render(vpcs=vpcs)
        print(msg)

if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('vpcs.j2')
    render_template(template, input_yaml_file='vpc_config.yml')

