output "s3_bucket_name" {
  description = "Name of the S3 bucket."
  value       = aws_s3_bucket.csv_bucket.bucket
}

output "sqs_main_queue_url" {
  description = "URL of the main SQS queue."
  value       = aws_sqs_queue.csv_main_queue.id
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic."
  value       = aws_sns_topic.csv_upload_topic.arn
}