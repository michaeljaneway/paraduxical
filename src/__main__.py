from GameController import GameController


if __name__ == "__main__":
    gc = GameController()

    try:
        gc.mainLoop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Caught, exiting program gracefully...")
