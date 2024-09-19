import time
import json
import sys

class NeuronusStore:
    """
    A simple in-memory key-value store with Time to Live (TTL) functionality.
    Supports saving and loading data from disk in JSON format.
    """

    def __init__(self):
        """
        Initializes the store with two dictionaries:
        - store: Holds key-value pairs.
        - time_to_live: Tracks expiration times (TTL) for keys.
        """
        self.store = {}
        self.time_to_live = {}
        self.analytics_store = {}

    def set(self, key, value):
        """
        Sets a key-value pair in the store. Removes TTL if the key is updated.
        Args:
            key (str): The key to set.
            value (any): The value to associate with the key.
        Returns:
            str: "OK" to indicate success.
        """
        self.store[key] = value
        self.record_command_access_pattern(key)
        if key in self.time_to_live:
            del self.time_to_live[key]
        return "OK"

    def get(self, key):
        """
        Retrieves the value for a given key. Removes the key if it has expired.
        Args:
            key (str): The key to retrieve.
        Returns:
            any: The value associated with the key, or None if the key doesn't exist or has expired.
        """
        self.record_command_access_pattern(key)
        if key in self.time_to_live and time.time() > self.time_to_live[key]:
            del self.store[key]
            del self.time_to_live[key]
            return None
        return self.store.get(key, None)

    def expire(self, key, seconds):
        """
        Sets a TTL for a given key, after which it will be automatically removed.
        Args:
            key (str): The key to set the TTL for.
            seconds (int): Number of seconds after which the key will expire.
        Returns:
            int: 1 if the TTL was set successfully, 0 if the key was not found.
        """
        
        self.record_command_access_pattern(key)
        if key in self.store:
            self.time_to_live[key] = time.time() + int(seconds)
            return 1
        return 0

    def delete(self, key):
        """
        Deletes a key from the store and its TTL if present.
        Args:
            key (str): The key to delete.
        Returns:
            int: 1 if the key was deleted, 0 if the key was not found.
        """
        self.record_command_access_pattern(key)
        if key in self.store:
            del self.store[key]
            if key in self.time_to_live:
                del self.time_to_live[key]
            return 1
        return 0

    def save_to_disk(self, filename='neuronus_local_store.rdb'):
        """
        Saves the current state of the store to a file in JSON format.
        Args:
            filename (str): The file to save the store to.
        """
        with open(filename, 'w') as f:
            json.dump(self.store, f)
        
        # Save analytics data to disk
        temp_analytics_store = []
        
        for key in self.analytics_store:
            value = self.analytics_store[key]
            temp_analytics_store.append({
                "key": key,
                "access_count": value["access_count"],
                "last_accessed": value["last_accessed"],
                "size": value["size"],
                "ttl": value["ttl"]
            })
            
        print('temp_analytics_store: ', temp_analytics_store)
        
        # Save the analytics data to a separate file
        with open('neuronus_analytics_store.rdb', 'w') as f:
            json.dump(temp_analytics_store, f)


    def load_from_disk(self, filename='neuronus_local_store.rdb'):
        """
        Loads the store from a file, if it exists.
        Args:
            filename (str): The file to load the store from.
        """
        try:
            with open(filename, 'r') as f:
                self.store = json.load(f)
        except FileNotFoundError:
            pass

    def record_command_access_pattern(self, key):
        """
        Logs the access pattern for each key. Tracks:
            - access count
            - time of last access
            - size of the key's value
            - current TTL of the key (if applicable)
        """
        value = self.store.get(key, None)
        
        if value is None:
            return
        
        if key not in self.analytics_store:
            self.analytics_store[key] = {
                "access_count": 1,
                "last_accessed": time.time(),
                "size": sys.getsizeof(value),
                "ttl": self.time_to_live.get(key, None)
            }
        else:
            self.analytics_store[key]["access_count"] += 1
            self.analytics_store[key]["last_accessed"] = time.time()
         

        self.analytics_store[key]["size"] = sys.getsizeof(value)
        self.analytics_store[key]["ttl"] = self.time_to_live.get(key, None)