# Inter-region s3 proxy demo


## Description
This sample demonstrates how to create a scalable s3 proxy that only requests data from another region once. 
The fastapi app, takes s3 rest requests, and get the head of the local s3 object first. If it is empty, it copies
the object from the origin s3 bucket to the local s3 bucket, and then returns it to the caller. This sample is uses the project [CI/CD pipeline for testing containers on AWS Fargate with scaling to zero](https://aws.amazon.com/blogs/containers/ci-cd-pipeline-for-testing-containers-on-aws-fargate-with-scaling-to-zero/)

## How to run this example

If you would like to try this example yourself, there is a cloud formation stack that can be run within your own AWS account. If your region is not listed, you can modify the launch link and replace with your region.

| Region | Launch Template |
|-|-|
| US East (N. Virginia) *us-east-1* |[![us-east-1 Cloud Formation Template](./images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=inter-region-s3-proxy&templateURL=https://aws-wwps-apj-iss-public-samples.s3.amazonaws.com/inter-region-s3-proxy/aws-autostart-pipeline.yaml)|
| Asia Pacific (Singapore) *ap-southeast-1* |[![ap-southeast-1 Cloud Formation Template](./images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=inter-region-s3-proxy&templateURL=https://aws-wwps-apj-iss-public-samples.s3.amazonaws.com/inter-region-s3-proxy/aws-autostart-pipeline.yaml)|
| Asia Pacific (Sydney) *ap-southeast-2* |[![ap-southeast-2 Cloud Formation Template](./images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=inter-region-s3-proxy&templateURL=https://aws-wwps-apj-iss-public-samples.s3.amazonaws.com/inter-region-s3-proxy/aws-autostart-pipeline.yaml)