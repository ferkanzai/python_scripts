# Fernando Carmona 
# 11/OCT/2019
# This script lists all the latest Amazon Linux, Amazon Linux 2 and Windows 2019 AMIs per region with a CNF mapping template format

import boto3, json

ec2 = boto3.client('ec2')

list_regions = [ec2.describe_regions()["Regions"][i]["RegionName"] for i in range(len(ec2.describe_regions()["Regions"]))]

for region in list_regions:
    try:
        ssm = boto3.client('ssm', region_name=region)
        linux_ami = ssm.get_parameters(
            Names=[
                '/aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-gp2'
            ]
        )['Parameters'][0]['Value']
        linux2_ami = ssm.get_parameters(
            Names=[
                '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
            ]
        )['Parameters'][0]['Value']
        windows_ami = ssm.get_parameters(
            Names=[
                '/aws/service/ami-windows-latest/Windows_Server-2019-English-Full-Base'
            ]
        )['Parameters'][0]['Value']
        print("{}:".format(region))
        print("  \"AMALINUX\": \"{}\"".format(linux_ami))
        print("  \"AMALINUX2\": \"{}\"".format(linux2_ami))
        print("  \"WINDOWS\": \"{}\"".format(windows_ami))
    except:
        #print("{} has not SSM endpoint".format(region))
        continue