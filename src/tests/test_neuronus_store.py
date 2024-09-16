import time
import asyncio
from server.data_store import NeuronusStore

def test_basic_store():
    store = NeuronusStore()
    assert store.set("foo", "bar") == "OK"
    assert store.get("foo") == "bar"
    assert store.delete("foo") == 1
    assert store.get("foo") is None

def test_time_to_live():
    store = NeuronusStore()
    assert store.set("foo", "bar")
    store.expire("foo", 1)  # Set TTL of 1 second
    time.sleep(2)  # Wait for the key to expire
    assert store.get("foo") is None
    
def test_delete():
    store = NeuronusStore()
    store.set("key3", "value3")
    assert store.delete("key3") == 1
    assert store.get("key3") is None
    
async def test_set_get():
    server = NeuronusStore()
    reader, writer = await asyncio.open_connection('127.0.0.1', 6379)
    writer.write(b'SET foo bar')
    await writer.drain()
    response = await reader.read(1024)
    assert response == b"OK"

def test_load_from_disk():
    store = NeuronusStore()
    store.set("foo", "bar")
    store.save_to_disk()  # Save the current state

    # Later, or after a restart
    store.load_from_disk()  # Load the saved state
    assert store.get("foo") == "bar"


test_basic_store()
test_time_to_live()
test_set_get()
test_delete()
test_load_from_disk()