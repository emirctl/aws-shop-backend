from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
)


class ProductServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Get manually created tables
        products_table = dynamodb.Table.from_table_name(self, "ProductsTable", "products")
        stocks_table = dynamodb.Table.from_table_name(self, "StocksTable", "stocks")

        api = apigateway.RestApi(
            self,
            "ProductServiceApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
        )

        lambda_env = {
            "PRODUCTS_TABLE": products_table.table_name,
            "STOCKS_TABLE": stocks_table.table_name
        }

        get_products_list = _lambda.Function(
            self,
            "GetProductsList",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="getProductsList.handler.main", # FolderName.FileName.FunctionName
            code=_lambda.Code.from_asset("../lambda"), # Add whole folder to include data/mock_data.py
            environment=lambda_env, # Add environment variables
        )

        get_products_by_id = _lambda.Function(
            self,
            "GetProductsById",
            runtime=_lambda.Runtime.PYTHON_3_11,         
            handler="getProductsById.handler.main", # FolderName.FileName.FunctionName
            code=_lambda.Code.from_asset("../lambda"), # Add whole folder to include data/mock_data.py
            environment=lambda_env, # Add environment variables
        )

        create_product = _lambda.Function(
            self,
            "CreateProduct",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="createProduct.handler.main",
            code=_lambda.Code.from_asset("../lambda"),
            environment=lambda_env,
        )


        # Grant access to tables

        products_table.grant_read_write_data(create_product)
        stocks_table.grant_read_write_data(create_product)

        products_table.grant_read_data(get_products_list)
        stocks_table.grant_read_data(get_products_list)
        
        products_table.grant_read_data(get_products_by_id)
        stocks_table.grant_read_data(get_products_by_id)

        products = api.root.add_resource("products")

        products.add_method(
            "GET",
            apigateway.LambdaIntegration(get_products_list)
        )

        products.add_resource("{productId}").add_method(
            "GET",
            apigateway.LambdaIntegration(get_products_by_id)
        )

        products.add_method(
            "POST",
            apigateway.LambdaIntegration(create_product)
        )
