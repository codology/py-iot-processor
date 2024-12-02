import socket
import struct

class SensorReader:
    def __init__(self, host="0.0.0.0", port=28355):
        self.host = host
        self.port = port

    def read_sensors(self):
        """Reads sensor data from a binary stream."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen(1)
            print(f"Listening on {self.host}:{self.port}")
            conn, _ = server.accept()
            with conn:
                print("Connection established.")
                data = conn.recv(12)  # Assuming 3 float values (4 bytes each)
                if len(data) == 12:
                    # Decode binary data into temperature, humidity, sunlight
                    temperature, humidity, sunlight = struct.unpack("fff", data)
                    return {
                        "temperature": round(temperature, 2),
                        "humidity": round(humidity, 2),
                        "sunlight": round(sunlight, 2)
                    }
                else:
                    raise ValueError("Invalid sensor data length")
