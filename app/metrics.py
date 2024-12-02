import boto3

class MetricsCollector:
    def __init__(self, namespace="IoTData", region_name="us-east-1"):
        self.cloudwatch_client = boto3.client("cloudwatch", region_name=region_name)
        self.namespace = namespace

    def publish_metric(self, metric_name, value, unit="None"):
        self.cloudwatch_client.put_metric_data(
            Namespace=self.namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": value,
                    "Unit": unit,
                },
            ]
        )
