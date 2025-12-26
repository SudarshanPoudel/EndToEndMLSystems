import asyncio
import json
import random
from aiokafka import AIOKafkaProducer

async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092", 
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    
    await producer.start()

    for _ in range(10):
        await producer.send_and_wait(
            "user_events", 
            key="user_1", 
            value={"video": "Video_01", "watch_time": random.randint(1, 15)}
        )

        await asyncio.sleep(2)
    
    await producer.stop()

asyncio.run(main())
