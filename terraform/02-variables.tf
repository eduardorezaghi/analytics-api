variable "aws_region" {
  description = "AWS region for the resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "A unique name for the project to prefix resources."
  type        = string
  default     = "analytics-api"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
  default     = "csv-processing-bucket"
}

variable "sqs_queue_name" {
  description = "The name of the SQS queue."
  type        = string
  default     = "csv-processing-queue"
}

variable "sqs_dlq_name" {
  description = "The name of the SQS dead-letter queue."
  type        = string
  default     = "csv-processing-dlq"
}

variable "sns_topic_name" {
  description = "The name of the SNS topic."
  type        = string
  default     = "csv-processing-topic"
}