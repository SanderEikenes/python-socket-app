import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 4000))
print(client.recv(1024).decode())
lastQuestionChecked = 0
while True:
    message = input('>')

    # Handle the message command
    match message:
        case "post":
            problem = input('Enter the problem: ')
            alternative1 = input('Enter the first alternative: ')
            alternative2 = input('Enter the second alternative: ')
            alternative3 = input('Enter the third alternative: ')
            client.send(f"POST_PROBLEM;{problem};{alternative1};{alternative2};{alternative3}".encode())
        case "list":
            client.send("GET_PROBLEMS".encode())
        case "get":
            questionId = input('Enter the question ID: ')
            client.send(f"GET_PROBLEM;{questionId}".encode())
        case "vote":
            questionId = input('Enter the question ID: ')
            alternative = input('Enter the alternative: ')
            client.send(f"VOTE;{questionId};{alternative}".encode())
        case "help":
            client.send("help".encode())

    # Read all incoming messages
    while True:
        try:
            client.settimeout(0.5)
            response = client.recv(1024).decode()
            parts = response.split(';')
            match parts[0]:
                case "PROBLEMS":
                    print(f"{parts[1]}: {parts[2]}")
                case "PROBLEM":
                    print(parts[2])
                    print(f"1. {parts[3]}, Votes: {parts[4]}")
                    print(f"2. {parts[5]}, Votes: {parts[6]}")
                    print(f"3. {parts[7]}, Votes: {parts[8]}")
                case "PROBLEM_CREATED":
                    print(f"Problem created with ID: {parts[1]}")
                case "VOTE_SUCCESS":
                    print("Voted")
                case "COMMANDS":
                    for part in parts[1:]:
                        print(part)
                case "ERROR":
                    print(parts[1])
            if not response:
                break
        except socket.timeout:
            break

    client.settimeout(None)