import boto3
import uuid
import os


dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

products_table = dynamodb.Table("products")
stocks_table = dynamodb.Table("stocks")

products = [
    {
        "id": str(uuid.uuid4()),
        "title": "Keyboard",
        "description": "Mechanical keyboard",
        "price": 120
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Mouse",
        "description": "Gaming mouse",
        "price": 80
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Monitor",
        "description": "27 inch monitor",
        "price": 300
    }
]

for product in products:
    products_table.put_item(Item=product)

    stocks_table.put_item(
        Item={
            "product_id": product["id"],
            "count": 10
        }
    )

print("Filled database")
