from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)


class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        api = apigateway.RestApi(
            self,
            "ProductServiceApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
        )

        get_products_list = _lambda.Function(
            self,
            "GetProductsList",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="getProductsList.handler.main", # FolderName.FileName.FunctionName
            code=_lambda.Code.from_asset("../lambda"), # Add whole folder to include data/mock_data.py
        )

        get_products_by_id = _lambda.Function(
            self,
            "GetProductsById",
            runtime=_lambda.Runtime.PYTHON_3_11,         
            handler="getProductsById.handler.main", # FolderName.FileName.FunctionName
            code=_lambda.Code.from_asset("../lambda"), # Add whole folder to include data/mock_data.py
        )

        products = api.root.add_resource("products")

        products.add_method(
            "GET",
            apigateway.LambdaIntegration(get_products_list)
        )

        products.add_resource("{productId}").add_method(
            "GET",
            apigateway.LambdaIntegration(get_products_by_id)
        )
