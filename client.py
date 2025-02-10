import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 4000))
print(client.recv(1024).decode())
lastQuestionChecked = 0
while True:
    message = input('>')
    if message.startswith('vote'):
        parts = message[5:].split(' ')
        newMessage = f'vote {lastQuestionChecked} {parts[0]}'
        client.send(newMessage.encode())
    elif message.startswith('get'):
        parts = message[4:].split(' ')
        lastQuestionChecked = parts[0]
        newMessage = f'get {parts[0]}'
        client.send(newMessage.encode())
    else:
        client.send(message.encode())

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