import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Create an IAM client
    iam_client = boto3.client('iam')
    ses_client = boto3.client('ses')

    # List all IAM users
    response = iam_client.list_users()

    # Extract user data from the response
    users = response['Users']
    user_data = []

    # Iterate over each user and extract relevant information
    for user in users:
        user_data.append({
            'Username': user['UserName'],
            'User ID': user['UserId'],
            'ARN': user['Arn'],
            'Created On': user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
        })
        user_name = user['UserName']
        access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        for key in access_keys:
            access_key_id = key['AccessKeyId']
            access_key_status = key['Status']
            access_key_created = key['CreateDate']
            access_key_expiry = access_key_created + timedelta(days=20)  # Set expiry to 90 days
            iam_user = iam_client.get_user(UserName=user_name)
            user_tags = iam_user['User'].get('Tags', [])

            for tag in user_tags:
                if tag['Key'] == 'email':
                    vall = tag['Value']
                    print(f"{vall}")
            if access_key_status == 'Active' and access_key_expiry.date() == datetime.now().date() + timedelta(days=7):
                # Send notification email to the user
                email_subject = "IAM Access Key Expiry Remainder Notification"
                email_body = f"Hello {user_name},\n\nYour IAM access key ({access_key_id}) will expire in 7 days. . Please rotate your access keys to ensure uninterrupted access to AWS resources.\n\nThank you."
                
                # Replace with your verified SES sender email address
                from_email = "aiazmohammed01@gmail.com"
                
                # Replace with the recipient's email address
                to_email = vall
                
                # Send email using Amazon SES
                ses_client.send_email(
                    Source=from_email,
                    Destination={
                        'ToAddresses': [to_email]
                    },
                    Message={
                        'Subject': {
                            'Data': email_subject
                        },
                        'Body': {
                            'Text': {
                                'Data': email_body
                            }
                        }
                    }
                )
            if access_key_status == 'Active' and access_key_expiry.date() <= datetime.now().date() + timedelta(days=7):
                # Send notification email to the user
                email_subject = "IAM Access Key Expiry Notification"
                email_body = f"Hello {user_name},\n\nYour IAM access key ({access_key_id}) has been revoked! Please create your access key to ensure uninterrupted access to AWS resources.\n\nThank you."
                
                # Replace with your verified SES sender email address
                from_email = "email@gmail.com"
                
                # Replace with the recipient's email address
                to_email = vall
                
                
                # Send email using Amazon SES
                ses_client.send_email(
                    Source=from_email,
                    Destination={
                        'ToAddresses': [to_email]
                    },
                    Message={
                        'Subject': {
                            'Data': email_subject
                        },
                        'Body': {
                            'Text': {
                                'Data': email_body
                            }
                        }
                    }
                )
                iam_client.delete_access_key(UserName=user_name, AccessKeyId=access_key_id)

    # Return the user data
    return {
        'statusCode': 200,
        'body': user_data
    }