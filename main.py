from core.brain import think
from voice.listener import listen


def main():
    print("J.A.R.V.I.S MARK I ONLINE.")
    print("Systems initialized.")
    print("Awaiting your command...\n")

    while True:
        command = listen()

        if command.lower() in {"exit", "quit", "shutdown"}:
            print("JARVIS: Shutting down. Goodbye.")
            break

        if command:
            response = think(command)
            print(f"JARVIS: {response}")


if __name__ == "__main__":
    main()