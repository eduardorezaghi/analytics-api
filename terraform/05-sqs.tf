resource "aws_sqs_queue" "csv_dlq" {
  name = "${var.sqs_dlq_name}"
}

resource "aws_sqs_queue" "csv_main_queue" {
  name = "${var.sqs_queue_name}"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.csv_dlq.arn
    maxReceiveCount     = 3
  })
}