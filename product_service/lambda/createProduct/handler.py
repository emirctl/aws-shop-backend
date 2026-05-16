import json
import boto3
import uuid
import os


dynamodb = boto3.client("dynamodb")

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
STOCKS_TABLE = os.environ["STOCKS_TABLE"]


def main(event, context):
    print(json.dumps(event))

    try:
        body = json.loads(event["body"])

        title = body.get("title")
        description = body.get("description", "")
        price = body.get("price")
        count = body.get("count")

        # Validation
        if (
            not title or
            not isinstance(price, int) or
            not isinstance(count, int)
        ):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Invalid product data"
                })
            }

        product_id = str(uuid.uuid4())

        dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": PRODUCTS_TABLE,
                        "Item": {
                            "id": {"S": product_id},
                            "title": {"S": title},
                            "description": {"S": description},
                            "price": {"N": str(price)}
                        }
                    }
                },
                {
                    "Put": {
                        "TableName": STOCKS_TABLE,
                        "Item": {
                            "product_id": {"S": product_id},
                            "count": {"N": str(count)}
                        }
                    }
                }
            ]
        )

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Product created",
                "id": product_id
            })
        }

    except Exception as e:
        print(str(e))

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Internal server error"
            })
        }