import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import * as cloudtrail from 'aws-cdk-lib/aws-cloudtrail'

export class LambdaEventBridge extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a Lambda function
    const lambdaFn = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: 'lambda-stache-secret.lambda_handler',
      code: lambda.Code.fromAsset('lambda/Stache-SecretsKey-Rotation'), 
    });

    // Create an IAM policy
    const iamPolicyLambda = new iam.PolicyStatement({
      actions: ['secretsmanager:GetSecretValue',
      'secretsmanager:ListSecrets',
      'secretsmanager:DescribeSecret'],
      resources: ['*'],
    });

    // const Cloudtrail = new cloudtrail.Trail(this, 'lambda-stach-trail')

    // Attach the IAM policy to the Lambda function's role
    lambdaFn.addToRolePolicy(iamPolicyLambda);

    // Create an EventBridge rule to trigger the Lambda function
    const rule = new events.Rule(this, 'SecrectsRetrieval', {
        eventPattern : {
            source: ["aws.secretsmanager"],
            detail: {
                eventSource: ["secretsmanager.amazonaws.com"],
                eventName : ["RotationSucceeded"]
            }
        }
    });

    // Add the Lambda function as a target for the EventBridge rule
    rule.addTarget(new targets.LambdaFunction(lambdaFn));
  }
}
