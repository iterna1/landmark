from threading import Thread


class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True, name='Server')

    def run(self):
        import server


class AppThread(Thread):
    def __init__(self):
        Thread.__init__(self, name='Application')

    def run(self):
        import app


def main():
    server_thread = ServerThread()
    app_thread = AppThread()

    server_thread.start()
    app_thread.start()


if __name__ == "__main__":
    main()
