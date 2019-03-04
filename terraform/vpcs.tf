module "vpc_tf_one" {
  source = "terraform-aws-modules/vpc/aws"

  cidr = "10.0.0.0/16"

  azs = [ "us-east-2a", "us-east2b" ]

  public_subnets  = [ 10.0.0.0/24, 10.0.1.0/24 ]
  private_subnets = [ 10.0.100.0/24, 10.0.100/24 ]

  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_s3_endpoint   = False

  enable_nat_gateway     = False
  single_nat_gateway     = False
  one_nat_gateway_per_az = false
}



module "vpc_tf_two" {
  source = "terraform-aws-modules/vpc/aws"

  cidr = "10.100.0.0/16"

  azs = [ us-east-2a, us-east2b ]

  public_subnets  = [ 10.100.0.0/24, 10.100.1.0/24 ]
  private_subnets = [ 10.100.100.0/24, 10.100.100/24 ]

  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_s3_endpoint   = True

  enable_nat_gateway     = True
  single_nat_gateway     = True
  one_nat_gateway_per_az = false
}
