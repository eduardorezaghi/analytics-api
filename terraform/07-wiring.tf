resource "aws_sns_topic_subscription" "sqs_subscription" {
  topic_arn = aws_sns_topic.csv_upload_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.csv_main_queue.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.csv_bucket.id

  topic {
    topic_arn     = aws_sns_topic.csv_upload_topic.arn
    events        = ["s3:ObjectCreated:Put"]
  }

  depends_on = [
    aws_sns_topic_policy.s3_publish_policy
  ]
}