# Client-Server Voting System

This project implements a simple client-server voting system using Python's socket programming. The client sends commands to the server, which processes them and sends back appropriate responses. The server can handle multiple types of requests, such as adding questions, listing questions, retrieving details, and voting on alternatives.

## Features

- **Server**:

  - Accepts commands from the client.
  - Allows users to submit questions with alternatives.
  - Supports listing questions.
  - Allows users to vote on alternatives for a question.
  - Sends responses back to the client based on the command received.

- **Client**:
  - Sends commands to the server.
  - Allows users to vote on questions and view alternatives.
  - Displays server responses to the user.

## Requirements

- Python 3.x
- No additional libraries are required; everything is built using Python's standard libraries (`socket`, `json`, `os`, `time`).

## How to Use

### Starting the Server:

1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project folder.
3. Run the server script:
   ```bash
   python server.py
   ```
   The server will start and listen for incoming client connections.

### Running the Client:

1. Open another terminal window.
2. Run the client script:
   ```bash
   python client.py
   ```
3. The client will connect to the server and prompt you for commands.

### Available Commands:

- **`help`**: Lists available commands.
- **`ask <question>;<alternative1>;<alternative2>;<alternative3>`**: Submits a new question with 3 alternatives.
- **`list`**: Lists all the questions available in the system.
- **`get <questionId>`**: Retrieves the details of a specific question (including alternatives and votes).
- **`vote <alternativeIndex>`**: Votes on an alternative for a specific question. NOTE: only works after first getting a question.

Example interaction:

1. **Add a question**:
   ```bash
   > ask What is your favorite color?;Red;Blue;Green
   Question submitted
   ```
2. **List available questions:**:
   ```bash
   > list
   ID: 1 Problem: What is your favorite color?
   ```
3. **Get details of a question**:
   ```bash
   > get 1
   Question: What is your favorite color?
    1: Red. Votes: 0
    2: Blue. Votes: 0
    3: Green. Votes: 0
   ```
4. **Vote on an alternative**:
   ```bash
   > vote 3
   Vote submitted
   ```

### Contributions

Feel free to open a PR if you find any bugs you want to fix, or features you want to improve :)
