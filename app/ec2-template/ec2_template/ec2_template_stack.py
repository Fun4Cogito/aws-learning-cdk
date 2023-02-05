import aws_cdk as cdk
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    
)
from constructs import Construct

with open("./user_data/settings.sh") as f:
    user_data = f.read()

class Ec2TemplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        private_security_group_id = cdk.Fn.import_value("Demo-PrivateSecurityGroupID")

        ec2_launch_template = ec2.LaunchTemplate(self, "DemoLaunchTemplate",
            # machine_image="ami-06ee4e2261a4dc5c3",
            machine_image=ec2.LookupMachineImage(
                name='amzn2-ami-kernel-5.10-hvm-2.0.20230119.1-x86_64-gp2',
                owners=["amazon"]
            ),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            key_name="appKeyPair",
            security_group=ec2.SecurityGroup.from_security_group_id(self, 'SG', private_security_group_id),
            user_data=ec2.UserData.custom(user_data)
        )

