# Fernando Carmona 
# 11/OCT/2019
# This script lists all the latest Amazon Linux AMIs per region with a CNF mapping template

import boto3, json

ec2 = boto3.client('ec2')

list_regions = [ec2.describe_regions()["Regions"][i]["RegionName"] for i in range(len(ec2.describe_regions()["Regions"]))]

for region in list_regions:
    try:
        ssm = boto3.client('ssm', region_name=region)
        ami = ssm.get_parameters(
            Names=[
                '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
            ]
        )['Parameters'][0]['Value']
        print("{}:".format(region))
        print("  \"AMALINUX\": \"{}\"".format(ami))
    except:
        #print("{} has not SSM endpoint".format(region))
        continue