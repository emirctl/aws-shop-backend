import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lambda')))

from getProductsList.handler import main


def test_get_products_list():
    event = {}
    response = main(event, {})
    assert response["statusCode"] == 200
    assert "body" in response
