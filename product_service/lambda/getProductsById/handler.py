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
        product_id = event['pathParameters']['productId']
        product = products_table.get_item(Key={'id': product_id}).get('Item')

        if not product:
            return {"statusCode": 404, "body": json.dumps({"message": "Product not found"})}
        
        stock = stocks_table.get_item(Key={'product_id': product_id}).get('Item', {})

        product['count'] = stock.get('count', 0)

        return {
            "statusCode": 200,
            "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Content-Type": "application/json"
            },
            "body": json.dumps(DecimalEncoder.encode(product))
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
