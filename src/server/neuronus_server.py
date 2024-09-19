import socket
import signal
import asyncio
import time
from data_store import NeuronusStore

class NeuronusServer:
    """
    A simple server that handles commands such as SET, GET, DEL, and EXPIRE.
    """

    def __init__(self, host="127.0.0.1", port=5002):
        """
        Initializes the server with the host and port for binding.
        """
        self.host = host
        self.port = port
        self.store = NeuronusStore()

    async def handle_client(self, reader, writer):
        """
        Handles client connections asynchronously, reads incoming commands, 
        and sends back appropriate responses.
        """
        addr = writer.get_extra_info('peername')
        print(f"Connected with {addr}")
        
        try:
            while True:
                try:
                    # Read incoming data
                    request = (await reader.read(1024)).decode('utf-8')
                    if not request:
                        break
                    
                    # Parse and execute the command
                    response = self.parse_command(request)
                    
                    # Send response to the client
                    writer.write((response + "\n").encode('utf-8'))
                    await writer.drain()
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError from {addr}: {e}")
                    break
        except asyncio.IncompleteReadError:
            pass
        finally:
            print(f"Connection closed with {addr}")
            writer.close()
            await writer.wait_closed()

    def parse_command(self, command):
        """
        Parses the command from the client and executes the appropriate method in the store.
        """
        parts = command.strip().split()
        if len(parts) == 0:
            return "ERR empty command"
        
        cmd = parts[0].upper()

        if cmd == 'SET':
            if len(parts) != 3:
                return "ERR wrong number of arguments for SET \n"
            key, value = parts[1], parts[2]
            
            return self.store.set(key, value)
        
        elif cmd == 'GET':
            if len(parts) != 2:
                return "ERR wrong number of arguments for GET \n"
            key = parts[1]
            value = self.store.get(key)
            return value if value else "nil"
        
        elif cmd == 'DEL':
            if len(parts) != 2:
                return "ERR wrong number of arguments for DEL"
            key = parts[1]
            return str(self.store.delete(key))
        
        elif cmd == 'EXPIRE':
            if len(parts) != 3:
                return "ERR wrong number of arguments for EXPIRE"
            key, seconds = parts[1], parts[2]
            return str(self.store.expire(key, seconds))

        return "Err unknown command"
        
    async def save_periodically(self, interval=90):
        """
        Saves the in-memory store to disk periodically at the given interval.
        """
        while True:
            print('Saving store to disk')
            self.store.save_to_disk()
            await asyncio.sleep(interval)
            
    async def cleanup_expired_keys(self, interval=120):
        """
        Cleans up expired keys from the store at regular intervals.
        """
        while True:
            now = time.time()
            expired_keys = [key for key, ttl in self.store.time_to_live.items() if ttl > now]
            
            for key in expired_keys:
                del self.store.delete[key]
                del self.store.time_to_live[key]
            await asyncio.sleep(interval)

    async def start_server(self):
        """
        Starts the server and listens for incoming client connections.
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        
        async with server:
            await server.serve_forever()

    async def shutdown(self, signal, loop):
        """
        Gracefully shuts down the server when an exit signal is received.
        """
        print(f"Received exit signal {signal.name}...")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        print("Cancelling outstanding tasks...")
        await asyncio.gather(*tasks, return_exceptions=True)
        loop.stop()
        

if __name__ == '__main__':
    # Initialize the event loop
    loop = asyncio.get_event_loop()

    # Create an instance of the server
    server = NeuronusServer()

    # Start the server and schedule periodic tasks
    loop.create_task(server.start_server())
    loop.create_task(server.save_periodically(interval=60))
    loop.create_task(server.cleanup_expired_keys(interval=60))

    # Register signal handlers for graceful shutdown
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(server.shutdown(s, loop)))

    # Run the event loop
    loop.run_forever()
