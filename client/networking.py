import socket
import pickle


class Server() :
    def __init__(self,
                HOST_IP:str,
                HOST_PORT:int,
                BUFF_SIZE:int,
                notify:bool = False) :

        self.BUFF_SIZE = BUFF_SIZE

        self.HOST_IP = HOST_IP
        self.HOST_PORT = HOST_PORT
        self.HOST = (self.HOST_IP, self.HOST_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.HOST)
        self.sock.listen()

        self.notify = notify

        if notify == True :
            print("Server Started, now listening at port " + str(self.HOST_PORT))


    def newClient(self) :
        self.CLIENT, self.CLIENT_ADDR = self.sock.accept()

        if self.notify == True :
            print("Connected to : ", self.CLIENT_ADDR)

        self.CLIENT.settimeout(1.0)

    
    def closeClient(self) :
        self.CLIENT.close()


    def receive(self) :
        data = b''

        while True :
            try :
                packet = self.CLIENT.recv(self.BUFF_SIZE)
            except :
                break
            
            data += packet

        data = pickle.loads(data)

        return data


    def send(self, data) :
        data = pickle.dumps(data)
        self.CLIENT.sendall(data)

    
    def getHost(self) :
        return self.HOST
        

    def getClient(self) :
        return self.CLIENT_ADDR

    
    def __del__(self) :
        print('\nStopping Server...')
        self.CLIENT.close()
        self.sock.close()


class Client() :
    def __init__(self,
                SERVER_IP:str,
                SERVER_PORT:int,
                BUFF_SIZE:int,
                notify:bool = False) :

        self.BUFF_SIZE = BUFF_SIZE

        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.SERVER = (self.SERVER_IP, self.SERVER_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.SERVER)

        if notify == True :
            print('Connected  to ', self.SERVER, ' Successfully')

    
    def receive(self) :
        data = self.sock.recv(self.BUFF_SIZE)
        data = pickle.loads(data)

        return data
        

    def send(self, data) :
        data = pickle.dumps(data)
        self.sock.sendall(data)


    def endSession(self) :
        self.sock.close()


    def getServer(self) :
        return self.SERVER


    def __del__(self) :
        self.sock.close()


def dumpToFile(data, file:str) :
    pickle.dump(data, open(file, 'wb'))


def loadFromFile(file:str) :
    return pickle.load(open(file, 'rb'))