#code adapted from Computer Networking: A Top Down Approach by Kurose and Ross
#from chapter 2.7
#https://docs.python.org/3.4/howto/sockets.html

from socket import *

#function to play rock paper scissors depending on whether client or server is the initator
def runGame(clientSocket, initiator):

    #when initating game
    if initiator == True:
        print('type (R)ock, (P)aper, or (S)cissors')
        print('type /q to quit')

        message = input(PROMPT)

        # while (message != QUIT or ((len(message) != 1) and (message not in 'RPS'))):
        #     print('Please enter a valid response from the mentioned options')
        #     message = input(PROMPT)

        if message == QUIT:
            print("Quitting game")
            clientSocket.send(message.encode())
            return

        #get win loss or tie from server
        clientSocket.send(message.encode())

        #check game victory condition
        response = clientSocket.recv(4096).decode()
        if response == 'W':
            print("You won!")
        if response == "L":
            print("You lost")
        if response == "T":
            print("Tie game")
        if response == QUIT:
            print("Quitting game")
            return

        print("Game over. Going back to chat")
        return

    if initiator == False:
        #when asked to play game
        print('Server wants to play a game')
        print('type (R)ock, (P)aper, or (S)cissors')
        print('type /q to quit')
        print('Please wait for input prompt before entering message...')

        response = clientSocket.recv(4096).decode()

        if response == QUIT:
            print("Server quitting game")
            return

        message = input(PROMPT)
        # while ((message != 'R') or (message != 'P') or (message != 'S') or (message != '/q') or (message == '')):
        #     print('Please enter a valid response from the mentioned options')
        #     message = input(PROMPT)

        result = ''

        #check if win loss or tie based on selections
        if message == 'P':
            if response == 'P':
                result = 'T'
            if response == 'S':
                result = 'L'
            if response == 'R':
                result = 'W'

        if message == 'S':
            if response == 'P':
                result = 'W'
            if response == 'S':
                result = 'T'
            if response == 'R':
                result = 'W'

        if message == 'R':
            if response == 'P':
                result = 'L'
            if response == 'S':
                result = 'W'
            if response == 'R':
                result = 'T'

        if result == 'W':
            print("You won!")
        if result == 'L':
            print("You lost")
        if result == 'T':
            print("Tie game")

        clientSocket.send(result.encode())
        print("Game over. Going back to chat")
        return

PROMPT = 'Enter input >'
QUIT = '/q'
GAME = '/rockpaperscissors'

#create socket to send request to
serverName = '127.0.0.1'
serverPort = 8001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print('connected to: ' + serverName + ' on port: ' + str(serverPort))
print('type /q to quit')
print('Enter message to send. Please wait for input prompt before entering message...')
print('Enter /rockpaperscissors to play a game of rock, paper, scissors')

message = input(PROMPT)

#decide what to do based on client input
while message == GAME:
    clientSocket.send(message.encode())
    runGame(clientSocket, True)
    message = input(PROMPT)

if message == QUIT:
    print("Shutting down")
    clientSocket.send(message.encode())
    clientSocket.close()


while (message == ''):
    print('An empty message is not valid. Please enter a valid message')
    message = input(PROMPT)

while(message != QUIT):
    clientSocket.send(message.encode())


    #get response
    response = clientSocket.recv(4096).decode()

    while response == GAME:
        runGame(clientSocket, False)
        response = clientSocket.recv(4096).decode()


    if response == QUIT:
        print("Server request shutdown. Shutting down")
        clientSocket.close()
        break

    print(response)

    message = input(PROMPT)

    #loop to keep going through client inputs and responses with server until quit
    while(message == GAME):
        clientSocket.send(message.encode())
        runGame(clientSocket, True)
        message = input(PROMPT)

    while (message == ''):
        print('An empty message is not valid. Please enter a valid message')
        message = input(PROMPT)

    if message == QUIT:
        print("Shutting down")
        clientSocket.send(message.encode())
        clientSocket.close()







