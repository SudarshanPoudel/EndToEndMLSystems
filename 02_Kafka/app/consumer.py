from kafka import KafkaConsumer


consumer = KafkaConsumer(
    "user_events", 
    bootstrap_servers="localhost:9092", 
    group_id="training_pipeline",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: v.decode("utf-8"),
)

print("Consumer started...")
for message in consumer:
    print(message.value)