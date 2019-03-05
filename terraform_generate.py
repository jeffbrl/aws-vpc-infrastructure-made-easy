#!/usr/bin/env python

import datetime
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.constructor import Constructor

# Don't convert string "true" and "false" to python True/False
def add_bool(self, node):
    return self.construct_scalar(node)

Constructor.add_constructor(u'tag:yaml.org,2002:bool', add_bool)


def file_exists(filename):
    file_handle = Path(filename)
    if file_handle.is_file():
        return True
    else:
        return False

def parse_vpcs(input_yaml_file):

    with open(input_yaml_file, 'r') as stream:
        try:
            vpcs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("===Invalid YAML===")
            print(exc)
            sys.exit(1)
    return vpcs

def write_tf_files(vpcs):
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('vpc.j2')
    for vpc in vpcs['Vpcs']:
      msg = template.render(vpc=vpc)
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
      output_file = f"terraform/{timestamp}-{vpc['name']}.tf"
      try:
          file_handle = Path(output_file)
          file_handle.write_text(msg)
      except Exception as e:
          print(f"unable to write to {output_file}")
          print(e)
          sys.exit(1)

if __name__ == '__main__':

    if not file_exists('vpc.j2'):
        print('unable to open jinja2 template file vpcs.j2')
        sys.exit(1)
    if not file_exists('vpc_config.yml'):
        print('unable to open YAML config file vpc_config.yml')
        sys.exit(1)

    vpcs = parse_vpcs(input_yaml_file='vpc_config.yml')
    write_tf_files(vpcs)

#    render_template(template, input_yaml_file='vpc_config.yml')

