import serial
import time
import optparse


SERIAL_PORT = '/dev/ttyUSB0'

def main():

    parser = optparse.OptionParser("exposer-send <options>");
    parser.add_option("-f","--file", action = "store", type="string", dest="g_code_file", help="G-Code Input File")

    (options, target) = parser.parse_args()

    # Open serial port
    s = serial.Serial(SERIAL_PORT, 9600)

    # Open g-code file
    f = open(options.g_code_file,'r');

    # Wake up open exposer
    s.write("\r\n\r\n")
    time.sleep(2) # Wait for open exposer to initialize
    s.flushInput() # Flush startup text in serial input

    # Stream g-code to grbl
    for line in f:
        l = line.strip() # Strip all EOL characters for streaming
        print "Sending: " + l,
        s.write(l + '\n') # Send g-code block to grbl
        grbl_out = s.readline() # Wait for open exposer response with carriage return
        print " : " + grbl_out.strip()

    # Wait here until open exopen exposer is finished to close serial port and file.
    raw_input("Press <Enter> to exit and disable open exoser.")

    # Close file and serial port
    f.close()
    s.close()

if __name__=="__main__":
    main()

