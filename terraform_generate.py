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

DEFAULT_YAML_FILE = 'vpc_config.yml'

logger = logging.getLogger("root")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='vpcs.log', format=FORMAT, level=logging.INFO)


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


def parse_vpcs(yaml_input_file):
    """ Parses VPC configuration from YAML file
    :param yaml_input_file: The YAML configuration file
    :type yaml_input_file: str
    :returns: dict representing the VPCs
    :rtype: dict
    """
    with open(yaml_input_file, "r") as stream:
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

    # create terraform files per vpc
    template = env.get_template("vpc.j2")
    outputs_tf_text = ""
    for vpc in vpcs["Vpcs"]:
        vpc_name = vpc['name']
        # generate the text for outputs.tf
        outputs_for_vpc =  (
        f'output {vpc_name} {{\n'
        f'  value = "${{module.{vpc_name}.vpc_id}}"\n'
        f'}}\n'
        )
        outputs_tf_text += outputs_for_vpc

        msg = template.render(vpc=vpc)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        vpc_terraform_file = f"terraform/{timestamp}-{vpc_name}.tf"
        try:
            file_handle = Path(vpc_terraform_file)
            file_handle.write_text(msg)
        except Exception as e:
            print(f"unable to write to {vpc_terraform_file}")
            print(e)
            sys.exit(1)
    try:
        outputs_file = f"terraform/{timestamp}-outputs.tf"
        file_handle = Path(outputs_file)
        file_handle.write_text(outputs_tf_text)
    except Exception as e:
        print(f"unable to write to {outputs_file}")
        print(e)
        sys.exit(1)

def validate_vpc_config(vpcs):
    """ Validate VPC configuration and log errors to file
    :param vpcs: dict representation of VPC configuration
    :type vpcs: dict
    :returns: True if VPC configuration is valid
    :rtype: bool
    """
    is_valid = True
    vpcs_to_check = vpcs['Vpcs']

    for vpc in vpcs_to_check:
        # AZs must match region
        for az in vpc['azs']:
            if not vpc['region'] in az: # e.g., us-east-1 not in eu-west-1a
                logger.error(f"{az} not in {vpc['region']}")
                is_valid = False
        # number of AZs must equal public and private subnet counts
        if len(vpc['azs']) != len(vpc['public_subnets']):
            logger.info(f"AZ count: {len(vpc['azs'])}")
            logger.info(f"public subnet count: {len(vpc['public_subnets'])}")
            logger.error('Number of AZs must equal number of public subnets')
            is_valid = False
        if len(vpc['azs']) != len(vpc['private_subnets']):
            logger.info(f"AZ count: {len(vpc['azs'])}")
            logger.info(f"private subnet count: {len(vpc['private_subnets'])}")
            logger.error('Number of AZs must equal number of private subnets')
            is_valid = False

    return is_valid


def main():
    logger.info('========================================')
    logger.info(f'{sys.argv[0]} executing at {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}')

    try:
        yaml_input_file = sys.argv[1]
    except IndexError:
        yaml_input_file = DEFAULT_YAML_FILE

    logger.info(f"yaml_input_file: {yaml_input_file}")
    if not file_exists("vpc.j2"):
        print("unable to open jinja2 template file vpcs.j2")
        return 1
    if not file_exists("vpc_config.yml"):
        print(f"unable to open YAML config file {yaml_input_file}")
        return 1

    vpcs = parse_vpcs(yaml_input_file=yaml_input_file)
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
