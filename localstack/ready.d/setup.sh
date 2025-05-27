#!/bin/bash
echo "---"
echo "--- Starting AWS resource creation ---"
echo "---"

# Globals
REGION="us-east-1"
S3_BUCKET_NAME="analytics-api-bucket"
SNS_TOPIC_NAME="csv-upload-topic"
SQS_QUEUE_NAME="csv-processing-queue"
SQS_DLQ_NAME="csv-processing-dlq"

# --- S3 ---
echo "---"
echo "--- Creating S3 bucket ---"
echo "---"
awslocal s3api create-bucket \
    --bucket $S3_BUCKET_NAME \
    --region $REGION

# --- SNS ---

echo "---"
echo "--- Creating SNS topic ---"
echo "---"
SNS_TOPIC_ARN=$(awslocal sns create-topic \
    --name $SNS_TOPIC_NAME \
    --query 'TopicArn' --output text)
echo " ------------------------- SNS Topic ARN: $SNS_TOPIC_ARN -------------------------"

# --- SQS ---
echo "---"
echo "--- Creating SQS queues ---"
echo "---"
DLQ_URL=$(awslocal sqs create-queue --queue-name $SQS_DLQ_NAME --attributes '{"MessageRetentionPeriod":"86400"}' --query 'QueueUrl' --output text)
DLQ_ARN=$(awslocal sqs get-queue-attributes --queue-url $DLQ_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
echo " ------------------------- DLQ ARN: $DLQ_ARN -------------------------"

echo "Creating main SQS queue..."
DEFAULT_QUEUE_ATTRIBUTES='{
  "VisibilityTimeout": "60",
  "MessageRetentionPeriod": "86400",
  "ReceiveMessageWaitTimeSeconds": "20",
  "RedrivePolicy": "{\"deadLetterTargetArn\":\"'"$DLQ_ARN"'\",\"maxReceiveCount\":\"3\"}"
}'
MAIN_QUEUE_URL=$(awslocal sqs create-queue \
    --queue-name $SQS_QUEUE_NAME \
    --attributes "$DEFAULT_QUEUE_ATTRIBUTES" \
    --query 'QueueUrl' --output text)
MAIN_QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url $MAIN_QUEUE_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
echo " ------------------------- Main Queue ARN: $MAIN_QUEUE_ARN -------------------------"

# --- Permissions & Subscriptions ---
echo "---"
echo "--- Creating permissions and subscriptions ---"
echo "---"
awslocal sns subscribe \
    --topic-arn $SNS_TOPIC_ARN \
    --protocol sqs \
    --notification-endpoint $MAIN_QUEUE_ARN

# echo "---"
# echo "--- Setting SQS queue policy to allow SNS to send messages ---"
# # Set the SQS queue policy to allow SNS to send messages

# awslocal sqs set-queue-attributes \
#     --queue-url $MAIN_QUEUE_URL \
#     --attributes '{
#       "Policy": "{
#         \"Version\": \"2012-10-17\",
#         \"Statement\": [
#           {
#             \"Effect\": \"Allow\",
#             \"Principal\": {
#               \"Service\": \"sns.amazonaws.com\"
#             },
#             \"Action\": \"SQS:SendMessage\",
#             \"Resource\": \"'"$MAIN_QUEUE_ARN"'\",
#             \"Condition\": {
#               \"ArnEquals\": {
#                 \"aws:SourceArn\": \"'"$SNS_TOPIC_ARN"'\"
#               }
#             }
#           }
#         ]
#       }"
#     }'
# echo " ------------------------- SNS Subscription ARN: $SNS_TOPIC_ARN -------------------------"


# --- Connect S3 to SNS ---
echo "Configuring S3 bucket to send notifications to SNS..."
awslocal s3api put-bucket-notification-configuration \
    --bucket $S3_BUCKET_NAME \
    --notification-configuration '{
        "TopicConfigurations": [
            {
                "TopicArn": "'"$SNS_TOPIC_ARN"'",
                "Events": ["s3:ObjectCreated:*"]
            }
        ]
    }'


# ---- Upload everything from ./.files/ directory to S3 bucket ----
echo "Uploading files to S3 bucket..."
for file in /etc/localstack/init/ready.d/.files/*; do
    awslocal s3 cp "$file" "s3://$S3_BUCKET_NAME/"
done

echo "---"
echo "--- AWS resource creation complete ---"
echo "---"
echo "---"
echo "---- Resource listings ----"
echo "--- S3 Buckets ---"
awslocal s3api list-buckets --query 'Buckets[].URL' --output text

echo "--- SNS Topics ---"
awslocal sns list-topics --query 'Topics[].TopicArn' --output text
echo "--- SQS Queues ---"
awslocal sqs list-queues --query 'QueueUrls' --output text
echo "--- SQS Queue Attributes ---"
awslocal sqs get-queue-attributes --queue-url $MAIN_QUEUE_URL --attribute-names All
echo "--- SQS DLQ Attributes ---"
awslocal sqs get-queue-attributes --queue-url $DLQ_URL --attribute-names All
echo "---"