from PIL import Image, ImageOps
import io

direction = {
    -1: None,
    0 : "N",
    1 : "E",
    2 : "S",
    3 : "W",
    4 : "NE",
    5 : "SE",
    6 : "SW",
    7 : "NW",
}

class Parser() :
    def __init__(self) :
        self.height = 0
        self.width = 0
        self.imgsrc = ''


    def parse(self, img:str) :
        mazeImage = Image.open(img)
        mazeImage = mazeImage.convert('LA')
        maze = list(mazeImage.getdata(0))
        
        for i in range(len(maze)) :
            if maze[i] == 0 :
                maze[i] = 1
            else :
                maze[i] = 0
        
        finalMaze = []

        self.width = mazeImage.size[0]
        self.height = mazeImage.size[1]
        self.imgsrc = img

        itr = 0

        while(itr < len(maze)) :
            temp = []

            for j in range(self.width) :
                temp.append(maze[itr])
                itr += 1

            finalMaze.append(temp)

        return finalMaze


    def getSize(self) :
        return (self.width, self.height)


class ImgManip() :
    def __init__(self) :
        self.frames = []

    def addToFrameBuffer(self, ps) :
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        self.frames.append(img)

    def saveAsGif(self, fileName:str = 'output') :
        fileName = fileName + '.gif'
        self.frames[0].save(fileName, save_all = True, append_images = self.frames[1:], duration = 100)
        