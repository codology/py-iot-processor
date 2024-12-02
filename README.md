## IoT Sensor Data Source Processor
Sensor data is read from a binary TCP stream on port `28355`. Each message contains three float values (12 bytes total):
1. **Temperature** (°C)
2. **Humidity** (%)
3. **Sunlight** (arbitrary units)

### Example Data Packet
- Binary format: `[Temperature (4 bytes)][Humidity (4 bytes)][Sunlight (4 bytes)]`
- Encoded as IEEE 754 floating-point values.

## Requirements
- Python3
- Docker
- AWS account with Kinesis stream set up
- AWS Secrets Manager to store secrets

## Layout
```bash
├── app/
│   ├── config.py
│   ├── metrics.py
│   ├── publisher.py
│   ├── sensors.py
│   └── __init__.py
├── tests/
│   ├── test_config.py
│   ├── test_metrics.py
│   ├── test_publisher.py
│   ├── test_sensors.py
│   └── __init__.py
├── Dockerfile
├── requirements.txt
├── README.md
└── run.sh
```

## Building
```bash
    docker build -t iot-kinesis-publisher .
```

## Testing
```bash
    docker run --rm iot-kinesis-publisher python -m unittest discover -s tests -p "*.py"

```

## Running the Application
Ensure the IoT device is sending data to the configured port before starting the Docker container.
```bash
    docker run -d --name iot-kinesis-publisher \
    -p 28355:28355 iot-kinesis-publisher \
    --stream-name your-stream-name \
    --region your-region \
    --secret-name your-secret-name

```
