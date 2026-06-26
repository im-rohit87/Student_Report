 id="ojgmsw"
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import QUIZ_FOLDER

import time


class QuizHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith(".csv"):

            print(
                f"New Quiz File Added: {event.src_path}"
            )

            try:

                from main import process_data

                process_data()

            except Exception as e:

                print(
                    f"Processing Error: {e}"
                )


def start_watcher():

    event_handler = QuizHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        QUIZ_FOLDER,
        recursive=False
    )

    observer.start()

    print(
        f"Watching folder: {QUIZ_FOLDER}"
    )

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()


if __name__ == "__main__":

    start_watcher()

