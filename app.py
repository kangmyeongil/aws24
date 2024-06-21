import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # 이벤트에서 이메일 주소 추출
    try:
        body = json.loads(event['body'])  # JSON 형식의 문자열을 파이썬 객체로 변환
        email = body['email']
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Failed to decode JSON body: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON body'})
        }

    # SES를 사용하여 이메일 보내기
    ses = boto3.client('ses', region_name='ap-northeast-2')
    sender_email = 'EMAIL'  # SES에서 인증된 이메일 주소 사용
    subject = 'Subscription Confirmation'
    body_text = f'Thank you for subscribing with email: {email}'

    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [email]},
            Message={'Subject': {'Data': subject}, 'Body': {'Text': {'Data': body_text}}}
        )
        print("SES send_email response:", response)
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error sending confirmation email'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Email sent successfully'})
    }
