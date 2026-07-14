import asyncio
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from display.manager import DisplayManager
from recordmate import RecordMate


async def main():

    display = DisplayManager()
    display.showFullScreen()

    app = RecordMate(display)

    await app.run()


if __name__ == "__main__":

    qt_app = QApplication(sys.argv)

    loop = QEventLoop(qt_app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.create_task(main())
        loop.run_forever()