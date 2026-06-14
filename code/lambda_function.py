import json
import boto3

s3 = boto3.client('s3')

def detect_object(image_name):

    image_lower = image_name.lower()

    if "dog" in image_lower:
        return [{"name": "dog", "confidence": 0.95}]

    elif "car" in image_lower:
        return [{"name": "car", "confidence": 0.92}]

    elif "person" in image_lower:
        return [{"name": "person", "confidence": 0.96}]

    elif "bicycle" in image_lower:
        return [{"name": "bicycle", "confidence": 0.91}]

    return [{"name": "unknown-object", "confidence": 0.75}]


def lambda_handler(event, context):

    # Works with both API Gateway and Lambda Test

    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    bucket_name = body['bucket']
    image_name = body['image']

    result = {
        "image": image_name,
        "objects": detect_object(image_name)
    }

    output_key = f"results/{image_name}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=json.dumps(result),
        ContentType='application/json'
    )

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }