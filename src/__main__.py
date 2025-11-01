from GameController import GameController
import os


if __name__ == "__main__":
    current_directory = os.getcwd()
    print(current_directory)
    
    gc = GameController()
    gc.mainLoop()
