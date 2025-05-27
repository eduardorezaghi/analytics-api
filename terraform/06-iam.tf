# This policy allows SNS to send messages to our SQS queue.
data "aws_iam_policy_document" "sqs_policy_for_sns" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.csv_main_queue.arn]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.csv_upload_topic.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "main_queue_policy" {
  queue_url = aws_sqs_queue.csv_main_queue.id
  policy    = data.aws_iam_policy_document.sqs_policy_for_sns.json
}