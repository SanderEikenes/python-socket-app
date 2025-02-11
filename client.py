import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 4000))
print(client.recv(1024).decode())
lastQuestionChecked = 0
while True:
    message = input('>')
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
            client.settimeout(0.5)  # Prevent infinite blocking
            response = client.recv(1024).decode()
            if not response:
                break
            print(response)
        except socket.timeout:
            break  # No more data, exit the loop

    client.settimeout(None)  # Reset timeout to default (blocking)