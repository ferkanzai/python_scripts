# This script will automatically change the Access and Secret key for all IAM users in the account if they're older than 90 days
# In order to work, change the profile_name in line 10, to the one you want to check

# thing to add: STS call to know exactly which user the profile uses and only modify that one in the credentials file
# if not, every user changes its credentials but the last one is kept in the file (and could be the wrong key)

# add Windows credential file change

import boto3, json, datetime, platform, os, re

os_type = platform.system()
now = datetime.datetime.now(datetime.timezone.utc)
#print(now)

with open('/Users/fca/.aws/credentials') as creds:
    lines = str(creds.readlines())
    #print(lines)
    profiles = re.findall('\[([A-Za-z]*)\]', lines)

print('Profiles configured in this laptop: {}'.format(profiles))

while True:
    profile = input('Which profile you want to change credentials for?\n')
    if profile not in profiles:
        print('not a valid profile, try again\n')
    else:
        break

session = boto3.Session(profile_name=profile)
iam = session.client('iam')
sts = session.client('sts')

user_profile = sts.get_caller_identity()['Arn'].split('/')[1]
#print(user_profile)
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
            if user == user_profile:
                os.system('aws configure set aws_access_key_id {} --profile {}'.format(new_access_key, profile))
                os.system('aws configure set aws_secret_access_key {} --profile {}'.format(new_secret_key, profile))
                print('Access key was changed to {} for {} profile'.format(new_access_key, profile))
            iam.delete_access_key(
                UserName=user,
                AccessKeyId=old_key
            )
            print('Old key {} was removed'.format(old_key))
        else:
            print('Credentials for user {} are newer than 90 days, no changes were made'.format(user))