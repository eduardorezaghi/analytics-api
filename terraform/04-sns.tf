# Defines the SNS topic that will receive notifications
resource "aws_sns_topic" "csv_upload_topic" {
  name = "csv-upload-topic"
}

# Creates the resource-based policy that allows S3 to publish to this topic
resource "aws_sns_topic_policy" "s3_publish_policy" {
  arn = aws_sns_topic.csv_upload_topic.arn

  # The policy document itself
  policy = data.aws_iam_policy_document.allow_s3_to_publish_to_sns.json
}

# Defines the policy document in a structured way
data "aws_iam_policy_document" "allow_s3_to_publish_to_sns" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }

    actions = ["sns:Publish"]

    # The resource this policy applies to (our topic)
    resources = [aws_sns_topic.csv_upload_topic.arn]

    # A crucial security condition: only allow our specific S3 bucket
    # to publish to this topic.
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.csv_bucket.arn]
    }
  }
}