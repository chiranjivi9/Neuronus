import time
import json

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
