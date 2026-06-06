import os
import json
import time
import random
from datetime import datetime, timezone
from google.cloud import pubsub_v1
from faker import Faker

# Initialize Faker and Pub/Sub Client
fake = Faker()
publisher = pubsub_v1.PublisherClient()

# Environment variables se config uthayein (Docker mai set karenge)
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "clickstream-raw")

# Full topic path build karein
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

# E-commerce elements simulation ke liye
EVENT_TYPES = ["view_item", "add_to_cart", "remove_from_cart", "view_category", "purchase"]
PAGE_URLS = [
    "/home", "/search?q=shoes", "/product/shoes-nike-air", 
    "/product/tshirt-adidas", "/cart", "/checkout/success"
]

print(f"Starting Clickstream Producer targeting topic: {topic_path}...")

try:
    while True:
        # 1. Fake event payload generate karein
        payload = {
            "session_id": f"sess_{random.randint(10000, 99999)}",
            "user_id": f"usr_{random.randint(100, 999)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": random.choice(EVENT_TYPES),
            "page_url": random.choice(PAGE_URLS),
            "ip_address": fake.ipv4()
        }
        
        # 2. Payload ko string/bytes mai convert karein
        data_bytes = json.dumps(payload).encode("utf-8")
        
        # 3. Pub/Sub par publish karein
        future = publisher.publish(topic_path, data_bytes)
        
        # Optional: Console par check karne ke liye output format print karein
        print(f"Published: {payload['event_type']} from {payload['ip_address']} -> Message ID: {future.result()}")
        
        # 4. Random delay (0.1 se 0.5 seconds) lagayein jaisa task mai manga hai
        time.sleep(random.uniform(0.1, 0.5))

except KeyboardInterrupt:
    print("\nProducer stopped manually.")
except Exception as e:
    print(f"An error occurred: {e}")