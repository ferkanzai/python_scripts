# Fernando Carmona 2019
# This script will check all running instances in all regions and display them, to check which regions have running instances

import boto3, json

ec2 = boto3.client('ec2')
list_regions = [ec2.describe_regions()["Regions"][i]["RegionName"] for i in range(len(ec2.describe_regions()["Regions"]))]

running_instances = []

for region in list_regions:
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[
            {
                'Name': 'instance-state-code',
                'Values': [
                    '16'
                ]
            }
        ]
    )
    if len(response['Reservations']) == 0:
            continue
    else:
        for reservation in response['Reservations']:
            instances = reservation['Instances']
            for instance in instances:
                i_id = instance['InstanceId']
                running_instances.append({'Region': region, 'Instance ID': i_id})
print(json.dumps(running_instances, indent=2))