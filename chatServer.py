#code adapted from Computer Networking: A Top Down Approach by Kurose and Ross
#from chapter 2.7
#import socket
from socket import *


#function to play rock paper scissors depending on whether client or server is the initator
def runGame(connectionSocket, initiator):

    #when server is the initator of game
    if initiator == True:
        print('type (R)ock, (P)aper, or (S)cissors')
        print('type /q to quit')

        message = input(PROMPT)
        # while ((message != "R") or (message != 'P') or (message != 'S') or (message != '/q') or (message == '')):
        #     print('Please enter a valid response form the mentioned options')
        #     message = input(PROMPT)

        if message == QUIT:
            print("Quitting game")
            connectionSocket.send(message.encode())
            return

        #send selection to client
        connectionSocket.send(message.encode())

        #client will respond back with who won or lost
        response = connectionSocket.recv(4096).decode()
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
        print('Client wants to play a game')
        print('type (R)ock, (P)aper, or (S)cissors')
        print('type /q to quit')
        print('Please wait for input prompt before entering message...')

        response = connectionSocket.recv(4096).decode()
        if response == QUIT:
            print("Client quitting game")
            return

        message = input(PROMPT)
        # while (message != QUIT or ((len(message) != 1) and (message not in 'RPS'))):
        #     print('Please enter a valid response from the mentioned options')
        #     message = input(PROMPT)
        print("input: " + message)

        result = ''

        #determine game results based on selections
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

        #send result to client
        connectionSocket.send(result.encode())
        print("Game over. Going back to chat")
        return

QUIT = '/q'
PROMPT = 'Enter input >'
GAME = '/rockpaperscissors'

#set up server socket
serverPort = 8001
serverIP = '127.0.0.1'
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print('Server listening on: ' + serverIP + ' port: ' + str(serverPort)  )
active = True


#accept requests
while active == True:
    connectionSocket, addr = serverSocket.accept()
    print('Connected by: ' + str(addr))
    print('Waiting for message...')

    response = connectionSocket.recv(4096).decode()

    while response == GAME:
        runGame(connectionSocket, False)
        response = connectionSocket.recv(4096).decode()

    if response == QUIT:
        active = False
        print("Client requested shutdown. Shutting down")
        connectionSocket.close()
        break

    print(response)


    print('type /q to quit')
    print('Enter /rockpaperscissors to play a game of rock, paper, scissors')
    print('Enter message to send. Please wait for input prompt before entering message...')


    message = input(PROMPT)

    #loop for server to keep sending inputs and getting responses until quit
    while(message != QUIT):
        while (message == ''):
            print('An empty message is not valid. Please enter a valid message')
            message = input(PROMPT)

        while(message == GAME):
            connectionSocket.send(message.encode())
            runGame(connectionSocket, True)
            message = input(PROMPT)

        if message == QUIT:
            print("Shutting down")
            active = False
            connectionSocket.send(message.encode())
            connectionSocket.close()
            break

        connectionSocket.send(message.encode())
        response = connectionSocket.recv(4096).decode()

        while response == GAME:
            runGame(connectionSocket, False)
            response = connectionSocket.recv(4096).decode()

        #if client wants to quit
        if response == QUIT:
            active = False
            print("Client requested shutdown. Shutting down")
            connectionSocket.close()
            break

        print(response)
        message = input(PROMPT)

    #if server wants to quit
    if message == QUIT:
        print("Shutting down")
        active = False
        connectionSocket.send(message.encode())
        connectionSocket.close()
        break







