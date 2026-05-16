import json
import os
import boto3
from common.utils import DecimalEncoder


# Reference: https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb.html

# Get dynamodb resource
dynamodb = boto3.resource('dynamodb')

# Get tables
products_table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])
stocks_table = dynamodb.Table(os.environ['STOCKS_TABLE'])


def main(event, context):
    # console.log
    print(f"Event: {json.dumps(event)}")

    try:
        all_products = products_table.scan()['Items']
        all_stocks = stocks_table.scan()['Items']

        # Join: Update stock information of products
        for product in all_products:
            product['count'] = 0 # default stock

            for stock in all_stocks:
                 if stock['product_id'] == product['id']:
                      product['count'] = stock['count']
        return {
            "statusCode": 200,
            "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Content-Type": "application/json"
            },
            "body": json.dumps(DecimalEncoder.encode(all_products))
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
