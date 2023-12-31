import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class LambdaSesStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a Lambda function
    const lambdaFn = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: 'lambda_function.lambda_handler',
      code: lambda.Code.fromAsset('lambda/IAM-Access-notification'), 
    });

    // Create an IAM policy
    const iamPolicy = new iam.PolicyStatement({
      actions: [
       'ses:SendEmail',
       'iam:ListAccessKeys', 
       'iam:GetAccessKeyLastUsed', 
       'iam:DeleteAccessKey',
       'iam:ListUser',
       'iam:GetUser'],
      resources: ['*'],
    });

    // Attach the IAM policy to the Lambda function's role
    lambdaFn.addToRolePolicy(iamPolicy);

    // Create an EventBridge rule to trigger the Lambda function
    const rule = new events.Rule(this, 'ScheduledRule', {
      schedule: events.Schedule.cron({ minute: '0', hour: '0' }), // Example: Run daily at midnight
    });

    // Add the Lambda function as a target for the EventBridge rule
    rule.addTarget(new targets.LambdaFunction(lambdaFn));
  }
}
