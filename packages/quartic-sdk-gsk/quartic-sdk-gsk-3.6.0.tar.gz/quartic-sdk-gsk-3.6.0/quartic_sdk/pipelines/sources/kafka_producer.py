from confluent_kafka.cimpl import Producer
import json
import os

class KafkaConnector(object):
    """
    Class to upload data to Kafka
    """

    def __init__(self):
        self.kafka_config = self.get_kafka_config()
        self.kafka_producer = Producer(self.kafka_config)

    
    def get_kafka_config(self):
        return {
                    'bootstrap.servers': os.environ.get('KAFKA_BROKER_URL', 'broker:9092'),
                    'sasl.mechanism': os.environ.get('KAFKA_SASL_MECHANISM'),
                    'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
                    'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
                    'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
                    'ssl.endpoint.identification.algorithm': ' ',
                    'message.timeout.ms': 30000,
                    'queue.buffering.max.ms': 50,
                    "topic.metadata.refresh.interval.ms": 180000,
                    'enable.ssl.certificate.verification': False,
                    'linger.ms': 50, 
                    'batch.size': 150000
                }

    async def upload_data(self, datapoint, topic, connector_id) -> None:
        """
        Transform message and write to Kafka
        """

        def delivery_callback(err, msg):
            if err:
                print(err)
            else:
                self.kafka_online = True

        self.kafka_producer.produce(topic, value=json.dumps(datapoint),
                                    key=str(connector_id), on_delivery=delivery_callback)