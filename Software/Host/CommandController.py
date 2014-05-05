__author__ = 'mariolukas'
from PolygonSlicer import PolygonSlicer
import time
import serial



class CommandController():

    serial_connection = 0
    slicer = 0

    def getLowByte(self, number):
        lobyte = chr(number % 256)
        return lobyte

    def getHighbyte(self, number):
        hibyte = chr(number / 256)
        return hibyte

    # protocol:  command | buffer length |  buffer
    #            1 byte  |  2 bytes      |  n bytes

    def sendData(self,command, data):
        buffer = []

        data.append(0)
        # 1 byte command
        buffer.append(command)

        buffer_len = len(data)

        # 2 byte buffer length
        buffer.append(self.getLowByte(buffer_len))
        buffer.append(self.getHighbyte(buffer_len))

        # data values as bytes

        for value in data:
            buffer.append(self.getLowByte(value))
            buffer.append(self.getHighbyte(value))

        #buffer.extend(['\x00','\x00'])

        self.serial_connection.write(buffer)


    def home_y_axis(self):
        data = []

        self.sendData('\x02',data)

        state = self.serial_connection.read(1)
        self.checkSerialResponse(state)

    def home_z_axis(self):
        data = []

        self.sendData('\x03',data)

        state = self.serial_connection.read(1)
        self.checkSerialResponse(state)

    def move_z_to_next_layer(self):
        data = []

        self.sendData('\x06',data)

        state = self.serial_connection.read(1)
        self.checkSerialResponse(state)

    def move_z_to_end_position(self):
        data = []

        self.sendData('\x08',data)

        state = self.serial_connection.read(1)
        self.checkSerialResponse(state)


    def checkSerialResponse(self,state):

        if (state):
            print "DONE"
        else:
            print "ERROR"

    def reset(self):
        self.serial_connection.setDTR(1)
        time.sleep(0.2)
        self.serial_connection.setDTR(0)

    def connect(self, port, speed):

        self.serial_connection = serial.Serial(port, speed, timeout=20)
        self.reset()
        #self.serial_connection.setDTR(False)
        time.sleep(2)   # Wait for grbl to initialize

        state = self.serial_connection.readline()
        print state

        self.serial_connection.flushInput()  # Flush startup text in serial input

    def disconnect(self):
        self.serial_connection.close()
        print "Connection closed"


    def loadFile(self, filename):
        self.slicer =  PolygonSlicer("resources/"+filename)

    def exposeLayer(self, layer):
        first_line = 0
        last_line = 0

        if(layer%2==0):
            first_line = 1
            last_line = self.slicer.getSVGHeight()
            count = 1
        else:
            first_line = self.slicer.getSVGHeight()
            last_line = 1
            count = -1

        for row in xrange(first_line,last_line, count):
                distances = self.slicer.getDistances(row,layer)

                self.sendData('\x01',distances)
                state = self.serial_connection.read(1)

                print str(distances)
                self.checkSerialResponse(state)

    def expose(self):

        for layer in xrange(0,self.slicer.countLayers()):
            self.exposeLayer(layer)
            self.move_z_to_next_layer()


