from argparse import ArgumentParser
from networking import Client
from agents import Agent
from random import choice
from parser import Parser
from time import time as currentTime

totalTimeStart = currentTime()

cmdArgs = ArgumentParser(description = 'Accepts a png image file as input for maze')
cmdArgs.add_argument('Path', metavar='path', type=str, help='Path to the png image file')
imgPath = cmdArgs.parse_args().Path

imgParser = Parser()
MAZE = imgParser.parse(imgPath)
Agent.setupEnvironment(MAZE)

noOfAgents = int(input('Number of Agents (Minimum 2) : '))
print()

START = []
GOAL = []

for i in range(noOfAgents) :
    print('AGENT', i+1)
    
    print('\tStart =>')
    sX = int(input('\t\tX : '))
    sY = int(input('\t\tY : '))

    print('\tGoal =>')
    gX = int(input('\t\tX : '))
    gY = int(input('\t\tY : '))

    sCoord = (sX, sY)
    gCoord = (gX, gY)

    START.append(sCoord)
    GOAL.append(gCoord)


sendingTimeStart = currentTime()

client = Client('15.206.191.18', 4005, 1024, notify = True)

client.send(MAZE)
print(client.receive())

client.send(START)
print(client.receive())

client.send(GOAL)
print(client.receive())

sendingTimeEnd = currentTime()

agents = []

for i in range(noOfAgents) :
    clr = '#' + ''.join(choice('0123456789ABCDEF') for i in range(6))
    agents.append(Agent(START[i], GOAL[i], color = clr))

client.send('\nCLIENT : Waiting for Directions')

print()
Agent.dumpCanvas

agentTimeStart = currentTime()

move = 1
while True :
    data = client.receive()
    if data == True :
        break
    else :
        print('Move', move, ' :\t', data)
        move += 1

        for i in range(noOfAgents) :
            agents[i].move(data[i])
    
        Agent.dumpCanvas()

agentTimeEnd = currentTime()

client.send('\nCLIENT : Directions Received')

print('\nGenerating Output Gif...\n')
Agent.genOutput('output')

totalTimeEnd = currentTime()

print('Total Execution Time     :', totalTimeEnd-totalTimeStart)
print('Time taken to Send Data  :', sendingTimeEnd-sendingTimeStart)
print('Time taken by the Agents :', agentTimeEnd-agentTimeStart)

print('\nEverything Done, Click on the Window to exit')
Agent.closeEnvironment()