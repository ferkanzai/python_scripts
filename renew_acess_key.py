# This script will automatically change the Access and Secret key for all IAM users in the account if they're older than 90 days
# In order to work, change the profile_name in line 10, to the one you want to check

import boto3, json, datetime, platform, os

os_type = platform.system()
now = datetime.datetime.now(datetime.timezone.utc)
#print(now)

session = boto3.Session(profile_name='personal')
iam = session.client('iam')

users = [user['UserName'] for user in iam.list_users()['Users']]

for user in users:
    access_keys = iam.list_access_keys(
        UserName=user
    )
    for access_key in access_keys['AccessKeyMetadata']:
        creation_time = access_key['CreateDate']
        old_key = access_key['AccessKeyId']
        #print(creation_time)
        #print(old_key)
        #diff = (now - creation_time).days
        #print(diff)
        if (now - creation_time).days >= 90:
            print('Credentials are older than 90, changing...')
            new_creds = iam.create_access_key(
                UserName=user
            )
            new_access_key = new_creds['AccessKey']['AccessKeyId']
            new_secret_key = new_creds['AccessKey']['SecretAccessKey']
            os.system('aws configure set aws_access_key_id {} --profile personal'.format(new_access_key))
            os.system('aws configure set aws_secret_access_key {} --profile personal'.format(new_secret_key))
            print('Access key was changed to {} for personal profile'.format(new_access_key))
            iam.delete_access_key(
                UserName=user,
                AccessKeyId=old_key
            )
            print('Old key {} was removed'.format(old_key))
        else:
            print('Credentials are newer than 90 days, no changes were made')