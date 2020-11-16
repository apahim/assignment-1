import json
import logging

import boto3


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

REGION = 'eu-west-1'
TAG = 'database'
DEST_CIDR_BLOCK = '10.10.10.10/32'

ec2 = boto3.client('ec2', region_name=REGION)


def lambda_handler(event, context):
    instances = ec2.describe_instances()
    # Getting all the instances of the database
    candidates = list()
    for instance in instances['Reservations']:
        for item in instance['Instances']:
            if 'Tags' not in item:
                continue
            for tag in item['Tags']:
                if tag['Key'] != TAG:
                    continue
                if tag['Value'] != 'true':
                    continue
                candidates.append(item['InstanceId'])

    status = ec2.describe_instance_status(InstanceIds=list(candidates))
    online = list()
    for instance_status in status['InstanceStatuses']:
        if instance_status['InstanceStatus']['Status'] == 'ok':
            online.append(instance_status['InstanceId'])

    if not online:
        msg = 'No online instances to work with'
        LOG.error(msg)
        return {
            'statusCode': 403,
            'body': json.dumps(msg)
        }

    route_tables = ec2.describe_route_tables()
    new_gw = online[0]
    for route_table in route_tables['RouteTables']:
        route_table_id = route_table['RouteTableId']

        if not is_database_rotue_table(route_table):
            continue

        current_route = None
        for route in route_table['Routes']:
            if route['DestinationCidrBlock'] != DEST_CIDR_BLOCK:
                continue
            current_route = route

        if current_route is None:
            ec2.create_route(DestinationCidrBlock=DEST_CIDR_BLOCK,
                             InstanceId=new_gw,
                             RouteTableId=route_table_id)
            # While on it, let's make sure to disable the SourceDestCheck
            # for all the online database instances
            ec2.modify_instance_attribute(
                InstanceId=new_gw,
                SourceDestCheck={'Value': False}
            )
            msg = (f'Added route on {route_table_id} '
                   f'to {DEST_CIDR_BLOCK} via {new_gw}')
            LOG.info(msg)
            return {
                'statusCode': 200,
                'body': json.dumps(msg)
            }

        if 'InstanceId' in current_route:
            current_gw = current_route['InstanceId']
            if current_gw in online:
                msg = (f'Route on {route_table_id} already '
                       f'pointing to {DEST_CIDR_BLOCK} '
                       f'via {current_gw}')
                LOG.info(msg)
                return {
                    'statusCode': 200,
                    'body': json.dumps(msg)
                }

        ec2.delete_route(DestinationCidrBlock=DEST_CIDR_BLOCK,
                         RouteTableId=route_table_id)
        ec2.create_route(DestinationCidrBlock=DEST_CIDR_BLOCK,
                         InstanceId=new_gw,
                         RouteTableId=route_table_id)
        # While on it, let's make sure to disable the SourceDestCheck
        # for all the online database instances
        ec2.modify_instance_attribute(
            InstanceId=new_gw,
            SourceDestCheck={'Value': False}
        )
        msg = (f'Updated route on {route_table_id} '
               f'to {DEST_CIDR_BLOCK} via {new_gw}')
        LOG.info(msg)
        return {
            'statusCode': 200,
            'body': json.dumps(msg)
        }


def is_database_rotue_table(route_table):
    for tag in route_table['Tags']:
        if tag['Key'] != TAG:
            continue
        if tag['Value'] != 'true':
            continue
        return True
    return False
