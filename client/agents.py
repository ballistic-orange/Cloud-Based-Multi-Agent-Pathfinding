import turtle
import random
from time import sleep as delay
from parser import ImgManip

#Object required to generate the output GIF defined here
imageManipulator = ImgManip()

#Dictionary to convert given Directions into respective coordinate changes
direction = {
    "N"  : ( 0,  1),
    "E"  : ( 1,  0),
    "S"  : ( 0, -1),
    "W"  : (-1,  0),
    "NE" : ( 1,  1),
    "SE" : ( 1, -1),
    "SW" : (-1, -1),
    "NW" : (-1,  1),
    None : ( 0,  0),
}

#Function to add individual elements of a tuple
def add(*tups:tuple) :
    rtup = [0,]*len(tups[0])
    
    for tup in tups :
        for i in range(0, len(tup)) :
            rtup[i] += tup[i]
    
    return tuple(rtup)

#Class defining the required functions and properties 
class Agent() :
    def __init__(self,
                start:[int, int],
                goal:[int, int],
                shape:str = 'circle',
                color:str = 'blue') :

        self.bot = turtle.Turtle(shape = shape)
        self.bot.hideturtle()
        self.bot.color(color)
        self.bot.pensize(1)
        self.bot.penup()

        self.start = start
        self.goal = goal
        self.pos = start
        
        self.bot.setposition(self.pos)
        self.bot.showturtle()        
        self.bot.pendown()
        turtle.update()

    def move(self, instruct: str) :
        if self.pos != self.goal :
            self.pos = add(self.pos, direction[instruct])
            self.bot.setposition(self.pos)
            turtle.update()

    @staticmethod
    def dumpCanvas() :        
        canvas = turtle.getcanvas()
        ps = canvas.postscript(colormode = 'color')
        imageManipulator.addToFrameBuffer(ps)

    @staticmethod
    def genOutput(filename:str) :
        imageManipulator.saveAsGif(filename)

    @staticmethod
    def setupEnvironment(maze) :
        rows = len(maze)
        cols = len(maze[0])
        turtle.setworldcoordinates(-1, -1, cols, rows)

        turtle.tracer(0, 0)
        turtle.delay(0)

        mazeDrawer = turtle.Turtle(shape = 'square')
        mazeDrawer.hideturtle()
        mazeDrawer.fillcolor('black')
        mazeDrawer.penup()
        mazeDrawer.speed(10)

        x_coord = 0
        y_coord = rows-1

        for row in maze :
            x_coord = 0
            for cell in row :
                if cell == 1 :
                    mazeDrawer.setposition(x_coord-0.5, y_coord+0.5)
                    mazeDrawer.begin_fill()
                    mazeDrawer.setposition(x_coord+0.5, y_coord+0.5)
                    mazeDrawer.setposition(x_coord+0.5, y_coord-0.5)
                    mazeDrawer.setposition(x_coord-0.5, y_coord-0.5)
                    mazeDrawer.end_fill()
                x_coord += 1
            y_coord -= 1

    @staticmethod
    def closeEnvironment() :
        turtle.Screen().exitonclick()

