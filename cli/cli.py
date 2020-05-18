import readline

class CommandLineInterface():
   
    def __init__(self):
        self.commands = {
            'hello' : self.hello, 
        }

        
    def prompt(self):
        return 'aurora > '
        

    def evaluate_command(self, command):
        # TODO make case insensitive

        if len(command) == 0:
            return None

        handler = self.commands.get(command[0])
        print('han:', handler)
        if handler is None:
            raise ValueError('Bad command')
 
        return handler(command[1:])


    def run_main_loop(self):
       while True:
           command = input(self.prompt()).split()

           try:
               response = self.evaluate_command(command)
               if response is not None:
                   print(response) 
           except ValueError:
               print('Unrecognized command')


    def hello(self, params):
        return 'hello'
 

