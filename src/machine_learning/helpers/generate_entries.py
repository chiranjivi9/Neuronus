#  Script to generate entries

import random
import string
import time
import json
from data_store import NeuronusStore  # Import your NeuronusStore class

# Define a pool of keys
key_pool = []

def generate_random_key():
    """Generate a random string key of length 5-10."""
    return ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))

def generate_random_value():
    """Generate a random string value of length 20-50."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(20, 50)))

def simulate_operations(store, num_operations=5000, new_key_ratio=0.3):
    """
    Simulate random operations on the store to generate access patterns.
    Args:
        store (NeuronusStore): Instance of NeuronusStore to perform operations on.
        num_operations (int): Number of operations to perform.
        new_key_ratio (float): Probability of generating a new key versus reusing an existing one.
    """
    global key_pool

    for _ in range(num_operations):
        try:
            # Choose a random operation
            operation_type = random.choice(['SET', 'GET', 'EXPIRE', 'DEL'])
            
            # Decide whether to use a new key or an existing key
            if random.random() < new_key_ratio or not key_pool:
                # Create a new key and add it to the pool
                key = generate_random_key()
                key_pool.append(key)
                print(f"New key generated: {key}")
            else:
                # Reuse an existing key
                key = random.choice(key_pool)
                print(f"Reusing key: {key}")

            # Perform the operation
            if operation_type == 'SET':
                value = generate_random_value()
                store.set(key, value)
                print(f"SET operation: Key = {key}, Value = {value}")
            
            elif operation_type == 'GET':
                result = store.get(key)
                if result is None:
                    print(f"GET operation: Key '{key}' not found or expired.")
                else:
                    print(f"GET operation: Key = {key}, Value = {result}")
            
            elif operation_type == 'EXPIRE':
                ttl = random.randint(100, 1000)  # Set a longer TTL to avoid premature expiration
                result = store.expire(key, ttl)
                if result == 0:
                    print(f"EXPIRE operation: Key '{key}' not found.")
                else:
                    print(f"EXPIRE operation: Key = {key}, TTL = {ttl} seconds")
            
            elif operation_type == 'DEL':
                result = store.delete(key)
                if result == 0:
                    print(f"DEL operation: Key '{key}' not found.")
                else:
                    print(f"DEL operation: Key = {key} deleted.")
                    key_pool.remove(key)  # Remove deleted key from the pool
            
            # Optional: Random sleep to simulate real access patterns
            time.sleep(random.uniform(0.01, 0.1))  # Simulate a small delay between operations

        except KeyError as ke:
            print(f"KeyError: {ke}")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        
        except TypeError as te:
            print(f"TypeError: {te}")
        
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")

def save_analytics_to_file(store, filename='generated_analytics.json'):
    """
    Save the analytics store to a file for later processing.
    Args:
        store (NeuronusStore): The store from which to save analytics data.
        filename (str): The name of the file to save analytics data to.
    """
    try:
        analytics_data = []
        for key, data in store.analytics_store.items():
            analytics_data.append({
                "key": key,
                "access_count": data["access_count"],
                "last_accessed": data["last_accessed"],
                "size": data["size"],
                "ttl": data["ttl"]
            })

        with open(filename, 'w') as f:
            json.dump(analytics_data, f, indent=4)
        print(f"Analytics data saved to {filename}")

    except Exception as e:
        print(f"Error saving analytics data: {e}")

if __name__ == "__main__":
    # Create an instance of NeuronusStore
    store = NeuronusStore()

    try:
        # Simulate operations to generate entries
        print("Simulating operations to generate entries...")
        simulate_operations(store, num_operations=5000, new_key_ratio=0.3)

        # Save the generated analytics data to a file for preprocessing
        save_analytics_to_file(store, filename='generated_analytics.json')

        print("Process completed. You can now preprocess the data.")
    
    except KeyboardInterrupt:
        print("Process interrupted. Saving progress before exiting...")
        save_analytics_to_file(store, filename='generated_analytics.json')
        print("Progress saved. Exiting...")
