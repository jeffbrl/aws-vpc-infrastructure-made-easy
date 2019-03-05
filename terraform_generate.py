#!/usr/bin/env python

import datetime
import logging
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.constructor import Constructor

# Don't convert string "true" and "false" to python True/False
def add_bool(self, node):
    return self.construct_scalar(node)


Constructor.add_constructor("tag:yaml.org,2002:bool", add_bool)


def file_exists(filename):
    """ Returns true if file exists
    :param filename: The file name to check
    :type  filename: str
    :returns: True if file exists
    :rtype: bool
    """
    file_handle = Path(filename)
    if file_handle.is_file():
        return True
    else:
        return False


def parse_vpcs(input_yaml_file):
    """ Parses VPC configuration from YAML file
    :param input_yaml_file: The YAML configuration file
    :type input_yaml_file: str
    :returns: dict representing the VPCs
    :rtype: dict
    """
    with open(input_yaml_file, "r") as stream:
        try:
            vpcs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("===Invalid YAML===")
            print(exc)
            sys.exit(1)
    return vpcs


def write_tf_files(vpcs):
    """ Creates terraform files using Jinja2 template
    :param vpcs: dict representation of VPC configuration
    :type vpcs: dict
    """
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("vpc.j2")
    for vpc in vpcs["Vpcs"]:
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


def validate_vpc_config(vpcs):
    """ Validate VPC configuration and log errors to file
    :param vpcs: dict representation of VPC configuration
    :type vpcs: dict
    :returns: True if VPC configuration is valid
    :rtype: bool
    """
    # unimplemented
    return True


def main():

    if not file_exists("vpc.j2"):
        print("unable to open jinja2 template file vpcs.j2")
        return 1
    if not file_exists("vpc_config.yml"):
        print("unable to open YAML config file vpc_config.yml")
        return 1

    vpcs = parse_vpcs(input_yaml_file="vpc_config.yml")
    if validate_vpc_config(vpcs):
        write_tf_files(vpcs)
    else:
        print(
            "Your YAML is valid but your VPC configuration is not. Check vpcs.log for troubleshooting"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
