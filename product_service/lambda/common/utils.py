from decimal import Decimal

class DecimalEncoder:
    @staticmethod
    def encode(obj):
        if isinstance(obj, list):
            return [DecimalEncoder.encode(i) for i in obj]
        if isinstance(obj, dict):
            return {k: DecimalEncoder.encode(v) for k, v in obj.items()}
        if isinstance(obj, Decimal):
            return int(obj)
        return obj