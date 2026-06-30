import boto3

def lambda_handler(event, context):

    ec2 = boto3.client('ec2')

    # Get all snapshots owned by this account
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all running EC2 instances
    instances_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    # Store all running instance IDs
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Check every snapshot
    for snapshot in response['Snapshots']:

        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        # If snapshot has no associated volume, delete it
        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot {snapshot_id} because no volume is associated.")
            continue

        try:
            # Get volume details
            volume_response = ec2.describe_volumes(
                VolumeIds=[volume_id]
            )

            volume = volume_response['Volumes'][0]

            # If volume is not attached to any instance
            if not volume['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted snapshot {snapshot_id} because volume is not attached.")

            else:
                instance_id = volume['Attachments'][0]['InstanceId']

                # If attached instance is not running
                if instance_id not in active_instance_ids:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted snapshot {snapshot_id} because instance is not running.")
                else:
                    print(f"Snapshot {snapshot_id} is still in use.")

        except ec2.exceptions.ClientError as e:

            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted snapshot {snapshot_id} because the volume no longer exists.")
            else:
                raise
