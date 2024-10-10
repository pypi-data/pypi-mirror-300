import os
import redis
import uuid
import json
import hashlib
import logging
from django.conf import settings
from cryptography.fernet import Fernet
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class RedisHelper:
    def __init__(self):
        redis_host = settings.REDIS_HOST
        redis_port = settings.REDIS_PORT 
        self.redis_clients = {
            'frontend': redis.StrictRedis(host=redis_host, port=redis_port, db=0),
            'oauth': redis.StrictRedis(host=redis_host, port=redis_port, db=1),
            'communications': redis.StrictRedis(host=redis_host, port=redis_port, db=2),
            'accounting': redis.StrictRedis(host=redis_host, port=redis_port, db=3),
            'track_n_trace': redis.StrictRedis(host=redis_host, port=redis_port, db=4),
            'ai_service': redis.StrictRedis(host=redis_host, port=redis_port, db=5),
            'masterdata_service': redis.StrictRedis(host=redis_host, port=redis_port, db=6),
            'reports_analysis': redis.StrictRedis(host=redis_host, port=redis_port, db=7),
            'shipping_logistics': redis.StrictRedis(host=redis_host, port=redis_port, db=8),
            'geo_location': redis.StrictRedis(host=redis_host, port=redis_port, db=9),
            'instant_messaging': redis.StrictRedis(host=redis_host, port=redis_port, db=10),
            'banking_integration': redis.StrictRedis(host=redis_host, port=redis_port, db=11),
            'mes': redis.StrictRedis(host=redis_host, port=redis_port, db=12),
            'vms': redis.StrictRedis(host=redis_host, port=redis_port, db=13),
            'erp': redis.StrictRedis(host=redis_host, port=redis_port, db=14),
            'crm': redis.StrictRedis(host=redis_host, port=redis_port, db=15),
            'help_desk': redis.StrictRedis(host=redis_host, port=redis_port, db=16),
            'payroll_service': redis.StrictRedis(host=redis_host, port=redis_port, db=17),
            'handshake': redis.StrictRedis(host=redis_host, port=redis_port, db=18),
        }

    def get_client(self, service=None):
        return self.redis_clients.get(service, self.redis_clients['frontend'])

    # Set the value in Redis
    def set_values(self, key, value, service=None):
        client = self.get_client(service)
        json_value = json.dumps(value)
        client.set(key, json_value)

    # Set the value in Redis with expiry time
    def set_values_with_expiry(self, key, value, expiry_time, service=None):
        client = self.get_client(service)
        try:
            client.setex(key, expiry_time, json.dumps(value))  # Ensure value is stored as JSON
            print(f"Key '{key}' set with a TTL of {expiry_time} seconds.")
        except Exception as e:
            print(f"Error setting key with expiry: {e}")

    # Get the value from Redis
    def get_value(self, key, service=None):
        client = self.get_client(service)
        json_value = client.get(key)
        if json_value:
            value = json.loads(json_value)
            return value
        return None

    # Delete key-value pair from Redis
    def delete_key(self, key, service=None):
        client = self.get_client(service)
        client.delete(key)

    # Generate UUID that will be used as a key in Redis
    def generate_uuid(self, data):
        has_string = hashlib.md5(data.encode("UTF-8")).hexdigest()
        generated_uuid = uuid.UUID(hex=has_string)
        return generated_uuid

    # Encrypt token using Fernet
    def encrypt_token(self, data):
        fernet = Fernet(os.getenv('ENCRYPT_DECRYPT_KEY'))
        encoded_token = fernet.encrypt(data.encode("UTF-8"))
        return encoded_token

    # Decrypt token using Fernet
    def decrypt_token(self, data):
        fernet = Fernet(os.getenv('ENCRYPT_DECRYPT_KEY'))
        decoded_token = fernet.decrypt(data).decode("UTF-8")
        return decoded_token

    # Redis lock implementation
    @contextmanager
    def redis_lock(self, lock_name, timeout=30):
        client = self.get_client()
        lock = client.lock(lock_name, timeout=timeout)
        if lock.acquire(blocking=True):
            try:
                yield
            finally:
                lock.release()
        else:
            raise Exception("Could not acquire lock")

    # Confirm Redis connection
    def confirm_connection(self, service=None):
        client = self.get_client(service)
        try:
            client.ping()
            return True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return False
   
    # # Confirm Redis connection
    # def confirm_connection(connection):
    #     try:
    #         connection.ping()
    #         return True
    #     except Exception as e:
    #         print(f"Redis connection failed: {e}")
    #         return False
