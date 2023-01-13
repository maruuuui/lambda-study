resource "aws_apigatewayv2_api" "lambda" {
  name          = "serverless_lambda_gw"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "serverless_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "hello_world" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.hello_world.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "hello_world_get" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
}

resource "aws_apigatewayv2_route" "hello_world_post" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "POST /"
  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
}

resource "aws_apigatewayv2_route" "hello_world_delete" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "DELETE /{id}"
  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_world.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_apigatewayv2_domain_name" "my_domain" {
  domain_name              = "album-api-mod.maruuuui.tk"

  domain_name_configuration {
    certificate_arn = "arn:aws:acm:ap-northeast-1:674302997061:certificate/c3c702cd-bc26-4ed0-95e0-d88766d4be46"
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "my_domain" {
  api_id      = aws_apigatewayv2_api.lambda.id
  domain_name = aws_apigatewayv2_domain_name.my_domain.id
  stage       = aws_apigatewayv2_stage.lambda.id
}

resource "aws_route53_record" "album-api" {
    zone_id = "Z09991593E0A5TCOI6DUX"
    name    = "album-api-mod.maruuuui.tk"
    type    = "A"

    alias {
        evaluate_target_health = true
        name                   = aws_apigatewayv2_domain_name.my_domain.domain_name_configuration[0].target_domain_name
        zone_id                = aws_apigatewayv2_domain_name.my_domain.domain_name_configuration[0].hosted_zone_id
    }
}
