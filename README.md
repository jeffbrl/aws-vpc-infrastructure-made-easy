
AWS VPC Infrastructure Made Easy
========

The purpose of these scripts is to simplify the creation of VPCs across all AWS regions. The VPCs are intended to be used
as sandboxes for testing and learning new AWS services. 

Users define the VPCs by writing a YAML configuration file. The script dynamically generates terraform configurations that rely
heavily on the 
[terraform-aws-vpc](https://github.com/terraform-aws-modules/terraform-aws-vpc) module. Any input described in the module's
documentation can be included in the VPC configuration. The `region` parameter is not an input to the module; however, it is a valid
parameter for the VPC configuration for this script to specifiy the AWS region.

## Installation

Requirements:
- python 3.6 or newer
- terraform 0.11

On Ubuntu 18.04 (x64):

```
sudo apt-get update
sudo apt-get install git build-essential unzip python3-pip
git clone https://github.com/jeffbrl/aws-vpc-infrastructure-made-easy.git
cd aws-vpc-infrastructure-made-easy
sudo pip3 install -r requirements.txt
# install terraform if not already installed
export VER="0.11.12"
wget https://releases.hashicorp.com/terraform/${VER}/terraform_${VER}_linux_amd64.zip \
-O /tmp/terraform_${VER}_linux_amd64.zip
unzip /tmp/terraform_0.11.12_linux_amd64.zip
sudo mv /tmp/terraform /usr/local/bin/terraform
sudo chown root:root /usr/local/bin/terraform
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
cp vpc_config.yml.sample vpc_config.yml
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
make init
make plan
make apply
```

To tear down the sandbox, execute `make destroy`.

