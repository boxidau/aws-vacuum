#!/usr/bin/env python

import boto3
from botocore import exceptions

print('Loading...')

regions = [
  'ap-southeast-2', 'us-east-1', 'us-west-2'
]


no_delete_tag = 'no_delete'
dry_run = True

def lambda_handler(event, context):

    for region in regions:
        print('Cleanup for region %s' % region)

        cleanup_ec2(region)
        #cleanup_rds(region)
    
#   print('    EC2 in %s' % region)
  
#   s3 = boto3.client('s3', region_name=region)

def cleanup_ec2(region):
    ec2 = boto3.resource('ec2', region_name=region)
    reservations = ec2.instances.all()

    for instance in reservations:
        print('- Checking %s' % instance.id)
        try:
            if any(d['Key'] == no_delete_tag for d in instance.tags):
                print(u'\u2713 Keeping %s' % instance.id)
                continue
        except TypeError:
            print('No tags for %s' % instance.id)

        print(u'\u267B Deleting %s' % instance.id)
        try:
            instance.terminate(DryRun=dry_run)
        except exceptions.ClientError as err:
            print(u'\u274C %s' % err.message)


def cleanup_rds(region):
    rds = boto3.client('rds', region_name=region)

    rds_instances = rds.describe_db_instances()

    for instance in rds_instances:
        print('- Checking %s' % instance.id)
        try:
            if any(d['Key'] == no_delete_tag for d in instance.tags):
                print(u'\u2713 Keeping %s' % instance.id)
                continue
        except TypeError:
            print('No tags for %s' % instance.id)

        print(u'\u267B Deleting %s' % instance.id)
        try:
            instance.terminate(DryRun=dry_run)
        except exceptions.ClientError as err:
            print(u'\u274C %s' % err.message)


if __name__ == "__main__":
    lambda_handler(None, None)
