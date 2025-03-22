from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class MyVpcStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC with only public subnets
        vpc = ec2.Vpc(
            self, "MyVpc",
            cidr="10.0.0.0/16",
            max_azs=2,  # Creates subnets across 2 availability zones
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="PublicSubnet1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=True
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="PublicSubnet2",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=True
                )
            ],
            nat_gateways=0  # No NAT Gateway since all subnets are public
        )

        # Explicitly define subnet CIDR ranges
        vpc.public_subnets[0].node.default_child.add_override("Properties.CidrBlock", "10.0.1.0/24")
        vpc.public_subnets[1].node.default_child.add_override("Properties.CidrBlock", "10.0.2.0/24")

        core.CfnOutput(self, "VpcId", value=vpc.vpc_id)
