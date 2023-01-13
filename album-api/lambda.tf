data "archive_file" "lambda_hello_world" {
  type = "zip"

  source_dir  = "${path.module}/hello_world"
  output_path = "${path.module}/hello_world.zip"
}

resource "aws_s3_object" "lambda_hello_world" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "hello-world.zip"
  source = data.archive_file.lambda_hello_world.output_path

  etag = filemd5(data.archive_file.lambda_hello_world.output_path)
}

resource "aws_lambda_function" "hello_world" {
  function_name = "HelloWorld"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_hello_world.key

  runtime = "python3.9"
  handler = "app.lambda_handler"

  source_code_hash = data.archive_file.lambda_hello_world.output_base64sha256

  role = aws_iam_role.lambda_exec.arn

  timeout = 10

  environment {
    variables = {
      ALLOW_ORIGIN = "http://album-app.maruuuui.tk"
      ENDPOINT_URL = "https://s3.ap-northeast-1.amazonaws.com"
      DYNAMO_ENDPOINT_URL = "https://dynamodb.ap-northeast-1.amazonaws.com"
      ACCESS_KEY_ID = "bar"
      SECRET_ACCESS_KEY = "bar"
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "hello_world" {
  name = "/aws/lambda/${aws_lambda_function.hello_world.function_name}"

  retention_in_days = 30
}
