import re
import json
from datetime import datetime
from jsonschema import FormatChecker
from flask_restx import fields

format_checker = FormatChecker()


@format_checker.checks("custom_date", ValueError)
def custom_date_check(value):
    datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return True


class CustomDateTime(fields.DateTime):
    __schema_format__ = "custom_date"
    __schema_example__ = "2019-03-07 15:40:01.000"

    def format(self, value: datetime):
        try:
            return datetime.strftime(value, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as e:
            raise fields.MarshallingError(e)


class GetLeadCategory(fields.Raw):
    __schema_type__ = "string"
    __schema_example__ = "A"

    def output(self, key, obj, ordered=False):
        category = obj.category
        if not category:
            rate = float(obj.conversion_score)
            category = 'A'
            if rate >= 0.4489113:
                category = 'A'
            elif rate >= 0.0869625:
                category = 'B'
            elif rate >= 0.029875346:
                category = 'C'
            elif rate >= 0:
                category = 'D'
        return category


class GetLeadMetadata(fields.Raw):
    __schema_type__ = "json"
    __schema_example__ = "{'key1': 'value1', 'key2': 2}"

    def output(self, key, obj, ordered=False):
        return obj.extra_data
