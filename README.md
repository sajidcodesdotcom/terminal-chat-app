# terminal-chat-app

This is a simple terminal-based realtime chat application built using socket library in Python.
The application allows multiple clients to connect to a server and send text messages to each other in real-time. If a user sends a text the text goes to the socket server and then socket server broadcast the message to all other connected users.

## Features

- Real-time message between multiple users.
- Total connected users updates on joining or leaving the chat.
- Allows to choose a name before starting the chat.
- Some cool terminal text effects.

## Requirements
- Python 3 or later
- `terminaltexteffects' library (for visual effects in the terminal)

# Installation

1. Clone the repository:

```bash
git clone https://github.com/sajidcodess/terminal-chat-app.git
```

2. Navigate to the project directory.
```bash
cd terminal-chat-app
```

3. Start the server.py in one terminal and client.py in different terminals.


3. Exiting the chat.
To exit the caht simply press `ctrl+c`.


Thank You.

