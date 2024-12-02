from sensors import SensorReader
from config import get_secret
from metrics import MetricsCollector
import boto3
import json
from time import sleep
import argparse

def publish_data(stream_name, region_name="us-east-1", secret_name="iot-kinesis-secrets"):
    secrets = get_secret(secret_name, region_name)
    kinesis_client = boto3.client("kinesis", region_name=region_name)
    metrics_collector = MetricsCollector(namespace="IoTData", region_name=region_name)
    sensor_reader = SensorReader()

    while True:
        try:
            data = sensor_reader.read_sensors()
            print(f"Publishing data: {data}")

            # Publish to Kinesis
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(data),
                PartitionKey="partition-key"
            )

            # Publish metrics
            metrics_collector.publish_metric("Temperature", data["temperature"], unit="None")
            metrics_collector.publish_metric("Humidity", data["humidity"], unit="Percent")
            metrics_collector.publish_metric("Sunlight", data["sunlight"], unit="None")

        except Exception as e:
            print(f"Error reading or publishing data: {e}")
        sleep(5)  # Wait before next read

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Publish IoT sensor data to AWS Kinesis and collect metrics.")
    
    parser.add_argument(
        "--stream-name", required=True, help="The name of the AWS Kinesis stream."
    )
    parser.add_argument(
        "--region", default="us-east-1", help="The AWS region (default: us-east-1)."
    )
    parser.add_argument(
        "--secret-name", default="iot-kinesis-secrets", help="The name of the AWS Secrets Manager secret (default: iot-kinesis-secrets)."
    )
    
    args = parser.parse_args()

    # Run the data publishing function with parsed arguments
    publish_data(args.stream_name, args.region, args.secret_name)