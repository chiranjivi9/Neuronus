# Neuronus - A Simple In-Memory Key-Value Store with TTL

Neuronus is a simple Redis-like key-value store implemented in Python. It supports basic operations such as `SET`, `GET`, `DEL`, and `EXPIRE`, along with Time to Live (TTL) functionality. The store can be saved to and loaded from disk in JSON format, making it a lightweight, persistent key-value store.

## ⚡ Features

- **SET**: Store a key-value pair.
- **GET**: Retrieve the value for a given key.
- **DEL**: Delete a key from the store.
- **EXPIRE**: Set a TTL (Time to Live) for a key, after which it will automatically be removed.
- **Persistence**: Save the current state of the store to disk and load it back on restart.

## 🛠️ How It Works

Neuronus consists of two main components:

1. **NeuronusStore**: The core in-memory key-value store that supports `SET`, `GET`, `DEL`, and `EXPIRE` commands. It manages key expiration through TTL and offers methods to save/load the store to/from disk.

2. **NeuronusServer**: The server that listens for client connections and processes commands asynchronously. It uses the `NeuronusStore` to perform operations and communicate with clients.

## 🖥️ Installation

### Prerequisites

- **Python 3.7+** installed on your machine.
- Basic understanding of Python, `asyncio`, and networking.

### 📦 Clone the Repository

git clone https://github.com/your-username/neuronus.git
cd neuronus

### 📥 Install Dependencies
To install dependencies, run the following command (if additional dependencies are added):

```
pip install -r requirements.txt
```
Note: For now, the project has no external dependencies.

### 🚀 Run the Server
```
python src/server/neuronus_server.py
```
The server will start on localhost:5002 by default.

### 🛠️ Interact with the Server
You can interact with the server using telnet or any socket-based client. For example, using telnet:
```
telnet 127.0.0.1 5002
```
Once connected, you can send commands like:

```
SET foo bar
GET foo
DEL foo
EXPIRE foo 10
```

## 💾 Persistence
Neuronus allows you to save the state of the key-value store to a file on disk and load it back on restart. By default, the store is saved to a file called neuronus_local_store.rdb.

- Save to disk: The store is saved periodically (every 60 seconds) or manually through the server's internal mechanisms.
- Load from disk: When the server starts, it automatically loads any saved store from the neuronus_local_store.rdb file.

## 🔍 Testing
Unit tests for the NeuronusStore class are provided in the tests directory.

To run the tests, use pytest:
```
pytest tests/test_neuronus_store.py
```

## 🤝 Contributing
If you’d like to contribute to Neuronus, feel free to open a pull request or report an issue in the GitHub repository.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.


## ✨ Customizing
Let me know if you'd like any further modifications! Let's collaborate and expand this project. 🚀🤝


