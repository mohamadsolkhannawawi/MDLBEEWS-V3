import json
import socket
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from utils.logger import get_logger

logger = get_logger("KafkaHelper")

def check_kafka_connection(bootstrap_servers: list[str]) -> bool:
    """
    Checks if Kafka brokers are reachable via TCP.
    """
    if not isinstance(bootstrap_servers, list):
        bootstrap_servers = [bootstrap_servers]
        
    logger.info(f"Checking Kafka connection to: {bootstrap_servers}")
    for server in bootstrap_servers:
        host, port = server.split(":")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, int(port)))
            if result == 0:
                logger.info(f"Successfully connected to Kafka broker at {server}")
                return True
        except Exception as e:
            logger.debug(f"Failed to connect to {server}: {e}")
        finally:
            sock.close()
    
    logger.warning("No Kafka brokers reachable.")
    return False

def topic_exists(topic_name: str, bootstrap_servers: list[str]) -> bool:
    """
    Checks if a Kafka topic exists.
    """
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        exists = topic_name in admin_client.list_topics()
        logger.debug(f"Topic '{topic_name}' exists: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking topic '{topic_name}': {e}")
        return False

def create_topic_if_not_exists(topic_name: str, num_partitions: int, replication_factor: int, bootstrap_servers: list[str]) -> None:
    """
    Creates a Kafka topic if it does not already exist. Blocks until successful.
    """
    while not check_kafka_connection(bootstrap_servers):
        sleep(3)
        
    while not topic_exists(topic_name, bootstrap_servers):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            new_topic = NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
            logger.info(f"Creating topic '{topic_name}'...")
            admin_client.create_topics(new_topics=[new_topic])
            logger.info(f"Topic '{topic_name}' created successfully.")
            break
        except Exception as e:
            if 'TopicAlreadyExistsError' in str(e) or 'already exists' in str(e):
                logger.info(f"Topic '{topic_name}' already exists, skipping creation.")
                break
            logger.error(f"Error creating topic '{topic_name}': {e}")
            sleep(3)

def get_producer(bootstrap_servers: list[str]) -> KafkaProducer:
    """
    Returns a configured KafkaProducer.
    """
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: json.dumps(v).encode('utf-8') if v else None
    )

def get_consumer(topic: str, group_id: str, bootstrap_servers: list[str]) -> KafkaConsumer:
    """
    Returns a configured KafkaConsumer.
    """
    return KafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )
