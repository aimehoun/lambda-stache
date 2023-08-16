#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { LambdaSesStack } from '../lib/lambda-ses-stack';
import { LambdaEventBridge } from '../lib/lambda-eventbridge-stack';

const app = new cdk.App();
new LambdaSesStack(app, 'LambdaSesStack',);
new LambdaEventBridge(app,'LambdaEventBridge',);