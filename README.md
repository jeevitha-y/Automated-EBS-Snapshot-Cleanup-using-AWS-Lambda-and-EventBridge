# Automated-EBS-Snapshot-Cleanup-using-AWS-Lambda-and-EventBridge

## Overview

This project automates the cleanup of stale Amazon EBS snapshots using AWS Lambda. The Lambda function is triggered by Amazon EventBridge on a scheduled basis to identify and delete snapshots associated with deleted or unused EBS volumes, helping reduce AWS storage costs.

---

## Architecture

```text
Amazon EventBridge (Schedule)
            │
            ▼
      AWS Lambda (Python)
            │
            ▼
 Amazon EC2 / Amazon EBS APIs
            │
            ▼
Delete Stale EBS Snapshots
```

---

## AWS Services Used

- AWS Lambda
- Amazon EventBridge
- Amazon EC2
- Amazon EBS
- AWS IAM
- Amazon CloudWatch Logs
- Python (Boto3)

---

## IAM Policy

Attach the following inline policy to the Lambda execution role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSnapshots",
        "ec2:DeleteSnapshot",
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes"
      ],
      "Resource": "*"
    }
  ]
}
```
## AWS Lambda Function
The AWS Lambda function is responsible for identifying stale Amazon EBS snapshots and deleting snapshots that are no longer associated with active EC2 instances or EBS volumes.
<img width="1920" height="823" alt="lambda" src="https://github.com/user-attachments/assets/fe06aafb-691e-4a18-94b1-0227c07c3182" />

---

## EventBridge Schedule

Use the following schedule expression to invoke the Lambda function automatically.
<img width="1920" height="880" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/140eff6b-c9b3-4edf-a9fe-38682eeb7f64" />


---

## Workflow

1. EventBridge triggers the Lambda function.
2. Lambda retrieves all EBS snapshots owned by the AWS account.
3. Lambda retrieves all running EC2 instances.
4. Lambda checks whether each snapshot's volume exists and is attached to a running EC2 instance.
5. Stale snapshots are deleted.
6. Execution logs are stored in Amazon CloudWatch Logs.

---

## Expected Output

- Deletes snapshots associated with deleted volumes.
- Deletes snapshots attached to unused or non-running EC2 instances.
- Preserves snapshots associated with active running EC2 instances.
  <img width="1920" height="861" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/30586341-0c86-4ccb-9a81-87560e212f83" />
  <img width="1920" height="1080" alt="Screenshot (15)" src="https://github.com/user-attachments/assets/b8549fd7-5955-4718-ac50-ca45a56981a0" />


