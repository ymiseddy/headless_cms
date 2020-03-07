"""
Headless CMS Application entry point.
"""
import sys
import shlex
import argparse

class Application:
    """ Main application """
    def run(self, argv):
        """ Runs the Headless CMS """
        parser = argparse.ArgumentParser(
            description="Headless CMS Application",
            usage=argv[0] + ''' <command> [<args>]

start       Starts running as a service.
console     Start the interactive console.
help        Displays this help message

''')
        parser.add_argument("command", nargs="?", default='console',
                            help="Command to run.")
        args = parser.parse_args(argv[1:2])

        if  not hasattr(args, 'command'):
            command = "console"
        else:
            command = args.command

        if command == 'help':
            parser.print_help()
            return 0

        exec_command = "_handle_" + command
        if not hasattr(self, exec_command):
            print("Unrecognized command.")
            parser.print_help()
            return -1
        cmd = getattr(self, exec_command)
        cmd(argv[2:])

        return 0

    def _handle_start(self, args):
        raise Exception("Not implemented yet.")

    def _handle_agent_add(self, args):
        pass
    
    def _handle_group_add_permission(self, args):
        pass

    def _handle_group_add(self, args):
        pass
    
    def _handle_group_permission_add(self, args):
        pass
    
    def _handle_agent_add_group(self, args):
        pass


    def _handle_console(self, args):
        print("Console mode activated.  Type quit to exit.")
        while True:
            line = input(">>")
            newargs = shlex.split(line)
            newargs.insert(0, '')
            if line == 'quit':
                break
            try:
                self.run(newargs)
            except Exception as e:
                print(e)

def run(argv):
    """ Runs the Headless CMS """
    app = Application()
    app.run(argv)

if __name__ == "__main__":
    run(sys.argv)
