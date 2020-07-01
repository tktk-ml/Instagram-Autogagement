from os import system, name
from .log import Log

class Screen():
    def clear():
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def welcomeAscii():
            Log.ascii('''
                _                                                    _   
     /\        | |                                                  | |  
    /  \  _   _| |_ ___   __ _  __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
   / /\ \| | | | __/ _ \ / _` |/ _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
  / ____ \ |_| | || (_) | (_| | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
 /_/    \_\__,_|\__\___/ \__, |\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                          __/ |       __/ |                              
                         |___/       |___/                                                                  
    ''')
