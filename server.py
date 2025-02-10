import socket
import json
import os
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 4000))
print('Server started')
server.listen(5)

DATABASE_FILE = 'database.json'
if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
    with open(DATABASE_FILE, 'r') as file:
        database = json.load(file)
else:
    database = []

while True:
    client, addr = server.accept()
    client.send("Connected to server".encode())
    print('Connection from', addr)
    
    while True:
        userMessage = client.recv(1024).decode()
        print(userMessage)
        match userMessage:
            case "bye":
                client.send("Goodbye".encode())
                client.close()
                break
            case "help":
                client.send("Commands: bye, help, ask, list, get, vote".encode())
            case _ if userMessage.startswith("ask"):
                parts = userMessage[4:].split(';')
                if len(parts) == 4 and all(parts):
                    question = parts[0]
                    alternative1 = parts[1]
                    alternative2 = parts[2]
                    alternative3 = parts[3]

                    new_entry = {
                        "questionId": len(database) + 1,
                        "question": question,
                        "alternatives": [{"alternative": alternative1, "votes": 0}, {"alternative": alternative2, "votes": 0}, {"alternative": alternative3, "votes": 0}]
                    }
                    database.append(new_entry)

                    with open(DATABASE_FILE, 'w') as file:
                        json.dump(database, file)

                    client.send("Question submitted".encode())
                else:
                    client.send("invalid format, it should look like this 'question;alternative1;alternative2;alternative3'".encode())
            case "list":
                if len(database) == 0:
                    client.send("No questions available".encode())
                else:
                    for index, entry in enumerate(database):
                        question = entry['question']
                        questionId = entry['questionId']
                        client.send(f'ID: {questionId} Problem: {question}'.encode())
                        time.sleep(0.1)
            case _ if userMessage.startswith("get"):
                questionId = int(userMessage[4:])
                for entry in database:
                    if entry['questionId'] == questionId:
                        question = entry['question']
                        alternatives = entry['alternatives']
                        client.send(f'Question: {question}'.encode())
                        time.sleep(0.1)
                        alternativeIndex = 1
                        for alternative in alternatives:
                            alternativeText = alternative['alternative']
                            votes = alternative['votes']
                            client.send(f'{alternativeIndex}: {alternativeText}. Votes: {votes}'.encode())
                            alternativeIndex += 1
                            time.sleep(0.1)
                        break
                else:
                    client.send("Question not found".encode())
            case _ if userMessage.startswith("vote"):
                # Format: vote <questionId> <alternativeIndex>
                parts = userMessage[5:].split(' ')
                if len(parts) == 2:
                    questionId = int(parts[0])
                    alternativeIndex = int(parts[1])
                    for entry in database:
                        if entry['questionId'] == questionId:
                            alternatives = entry['alternatives']
                            if 0 < alternativeIndex <= len(alternatives):
                                alternatives[alternativeIndex - 1]['votes'] += 1
                                with open(DATABASE_FILE, 'w') as file:
                                    json.dump(database, file)
                                client.send("Vote submitted".encode())
                            else:
                                client.send("Invalid alternative index".encode())
                            break
                    else:
                        client.send("Question not found".encode())
                else:
                    client.send("Invalid format. It should look like this 'vote <alternative>'".encode())
            case _:
                client.send("I don't understand".encode())        