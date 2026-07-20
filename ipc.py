from PySide6.QtNetwork import QLocalSocket


SERVER_NAME = "JarvisIPC"


def send_command(command: str):

    socket = QLocalSocket()

    socket.connectToServer(SERVER_NAME)

    if not socket.waitForConnected(500):
        return False

    socket.write(command.encode())

    socket.flush()
    socket.waitForBytesWritten()

    socket.disconnectFromServer()

    return True