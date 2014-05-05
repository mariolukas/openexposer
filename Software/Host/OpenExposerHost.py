from CommandController import CommandController
import cmd, sys

class OpenExposerHost(cmd.Cmd):
    prompt = 'exposer: '
    intro = "OpenExposer Host. Use 'help' for command list"

    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'
    command_controller = CommandController()

    def do_connect(self, line):
        port = '/dev/tty.usbserial-AH00ZJP0'
        speed = 115200
        self.command_controller.connect(port, speed)

    def do_disconnect(self, line):
        self.command_controller.disconnect()

    def do_home(self, arg):
        if (self.parse(arg)[0] == 'y'):
            self.command_controller.home_y_axis()

        if (self.parse(arg)[0] == 'z'):
             self.command_controller.home_z_axis()

        if (self.parse(arg)[0] == 'all'):
            self.command_controller.home_y_axis()
            self.command_controller.home_z_axis()

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '

    def do_loadfile(self, arg):
        self.command_controller.loadFile(self.parse(arg)[0])

    def do_exposelayer(self,arg):
        self.command_controller.exposeLayer(self.parse(arg)[0])

    def do_movetonextlayer(self,line):
        self.command_controller.move_z_to_next_layer()


    def do_test(self,line):
        port = '/dev/tty.usbserial-AH00ZJP0'
        speed = 115200
        self.command_controller.connect(port, speed)
        self.command_controller.home_y_axis()
        self.command_controller.home_z_axis()
        self.command_controller.loadFile("cube.svg")
        self.command_controller.expose()
        #self.command_controller.exposeLayer(50)
        #self.command_controller.home_y_axis()



    def do_EOF(self, line):
        return True

    def parse(self, arg):
        'Convert a series of zero or more numbers to an argument tuple'
        return  arg.split()

if __name__ == '__main__':
    OpenExposerHost().cmdloop()