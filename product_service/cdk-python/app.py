#!/usr/bin/env python3

import aws_cdk as cdk
from cdk_python.product_service_stack import ProductServiceStack

app = cdk.App()

ProductServiceStack(
    app,
    "ProductServiceStack",
    env=cdk.Environment(
    region="us-east-1"
    )
)

app.synth()