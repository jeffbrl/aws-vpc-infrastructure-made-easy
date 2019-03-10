
AWS VPC Infrastructure Made Easy
========

The purpose of these scripts is to simplify the creation of VPCs across all AWS regions. The VPCs are intended to be used
as sandboxes for testing and learning new AWS services. 

Users define the VPCs writing a YAML configuration file. The configuration serves as input to the 
[terraform-aws-vpc](https://github.com/terraform-aws-modules/terraform-aws-vpc) module. Any input described in the module's
documentation can be included in the VPC configuration. The `region` parameter is not an input to the module; however, it is a valid
parameter for the VPC configuration for this script to specifiy the AWS region.

## Installation

Requirements:
- python 3.6 or newer
- terraform 0.11

On Ubuntu 18.04 (x64):

Install terraform as described in this [blog](https://computingforgeeks.com/how-to-install-terraform-on-ubuntu-centos-7/).

```
sudo apt-get install git make
# clone the repo
git clone https://github.com/jeffbrl/aws-vpc-infrastructure-made-easy.git
cd aws-vpc-infrastructure-made-easy
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
```


## Run with sample data
I've included a sample YAML configuration file
```
Vpcs:
  - name: red
    region: us-east-1
    cidr_range: 10.0.0.0/16
    azs: [ us-east-1a, us-east-1b ]
    public_subnets: [ 10.0.0.0/24, 10.0.1.0/24 ]
    private_subnets: [ 10.0.100.0/24, 10.0.101.0/24 ]
    enable_s3_endpoint: false
    enable_nat_gateway: false
  - name: black
    region: us-west-1
    cidr_range: 10.100.0.0/16
    azs: [ us-west-1a, us-west-1b ]
    public_subnets: [ 10.100.0.0/24, 10.100.1.0/24 ]
    private_subnets: [ 10.100.100.0/24, 10.100.101.0/24 ]
    enable_s3_endpoint: true
    enable_nat_gateway: false

```

You can build the sandbox using the following steps.
```
make generate
make plan
make apply
```

To tear down the sandbox, execute `make destroy`.

