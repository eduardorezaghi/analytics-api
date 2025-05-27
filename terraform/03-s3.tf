resource "aws_s3_bucket" "csv_bucket" {
  bucket = "${var.project_name}-bucket"
}