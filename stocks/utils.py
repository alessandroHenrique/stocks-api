import boto3
import json
import logging
from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger("stocks")


def invoke_lambda(service_name, payload):
    """
    Calls an AWS Lambda function and returns the response.
    """
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=service_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    return json.loads(response["Payload"].read())


def get_last_valid_day():
    """
    Returns the last valid trading day (ignores weekends).
    """
    current_date = timezone.localtime().date() - timedelta(days=1)
    while current_date.weekday() in [5, 6]:
        current_date -= timedelta(days=1)
    logger.debug(f"Last valid trading day: {current_date.isoformat()}")
    return current_date.isoformat()
