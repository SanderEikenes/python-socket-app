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
        parts = userMessage.split(';')
        match parts[0]:
            case "help":
                client.send("COMMANDS;ask;help;vote;get;list".encode())
            case "POST_PROBLEM":
                if len(parts) == 5 and all(parts):
                    question = parts[1]
                    alternative1 = parts[2]
                    alternative2 = parts[3]
                    alternative3 = parts[4]
                    questionId = len(database) + 1
                    new_entry = {
                        "questionId": questionId,
                        "question": question,
                        "alternatives": [{"alternative": alternative1, "votes": 0}, {"alternative": alternative2, "votes": 0}, {"alternative": alternative3, "votes": 0}]
                    }
                    database.append(new_entry)

                    with open(DATABASE_FILE, 'w') as file:
                        json.dump(database, file)

                    client.send(f"PROBLEM_CREATED;{questionId}".encode())
                else:
                    client.send("ERROR;INVALID_FORMAT".encode())
            case "GET_PROBLEMS":
                if len(database) == 0:
                    client.send("ERROR;NO_QUESTIONS".encode())
                else:
                    for index, entry in enumerate(database):
                        question = entry['question']
                        questionId = entry['questionId']
                        client.send(f'PROBLEMS;{questionId};{question}'.encode())
                        time.sleep(0.1)
            case "GET_PROBLEM":
                questionId = int(parts[1])
                for entry in database:
                    if entry['questionId'] == questionId:
                        question = entry['question']
                        alternatives = entry['alternatives']
                        problem_text = f"PROBLEM;{questionId};{question}"
                        for alternative in alternatives:
                            alternativeText = alternative['alternative']
                            votes = alternative['votes']
                            problem_text += f";{alternativeText};{votes}"
                        client.send(problem_text.encode())
                        break
                else:
                    client.send("ERROR".encode())
            case "VOTE":
                # Format: vote <questionId> <alternativeIndex>
                if len(parts) == 3:
                    questionId = int(parts[1])
                    alternativeIndex = int(parts[2])
                    for entry in database:
                        if entry['questionId'] == questionId:
                            alternatives = entry['alternatives']
                            if 0 < alternativeIndex <= len(alternatives):
                                alternatives[alternativeIndex - 1]['votes'] += 1
                                with open(DATABASE_FILE, 'w') as file:
                                    json.dump(database, file)
                                client.send(f"VOTE_SUCCESS;{questionId};{alternativeIndex}".encode())
                            else:
                                client.send("ERROR;INVALID_INDEX".encode())
                            break
                    else:
                        client.send("ERROR;QUESTION_NOT_FOUND".encode())
                else:
                    client.send("ERROR;INVALID_FORMAT".encode())
            case _:
                client.send("I don't understand".encode())        