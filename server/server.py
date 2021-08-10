from networking import Server, loadFromFile, dumpToFile
import pathfinding as pf
from subprocess import run
from time import sleep as delay

SECS = 1

run('clear')
server = Server('172.31.5.50', 4005, 1024, notify = True)

def serverTasks() :
    print('\tWaiting for new Client....')
    server.newClient()

    run('clear')
    maze = server.receive()    
    server.send('\nSERVER : Maze Received')

    if maze == [] :
        maze = loadFromFile('maze.arr')
        print("\nUsing Local Maze :\n")
    else :
        dumpToFile(maze, 'maze.arr')
        print("\nNew Maze Provided :\n")

    starts = server.receive()
    server.send('\nSERVER : Starting Coordinates Received')
    print('\nStarting Coordinates : ', starts)

    ends = server.receive()
    server.send('\nSERVER : Ending Coordinates Received')
    print('Ending Coordinates   : ', ends)

    print(server.receive())

    try :
        directions = pf.getDirections(maze, starts, ends, 'astar')
    except :
        directions = [[None]*len(starts)]
    finally :
        for eachDirect in directions :
            server.send(eachDirect)
            print(eachDirect)
            delay(SECS)

    allSent = True
    server.send(allSent)

    lastMsg = server.receive()
    print(lastMsg)
    
    server.closeClient()
    run('clear')

while True :
    if serverTasks() == False :
        break