import logging
import time
from datetime import datetime

from workers.editor import Editor
from workers.listener import Listener
from items.manual import Manual
from workers.writer import Writer


class Manager:
    """
    Someone who manage listener and writer.
    """

    def __init__(self,  manual: Manual):
        """
        :param manual: The manual that defined how to help the server writing his diary.
                       Please see @manual.Manual
        """
        self.manual = manual
        self.listener = Listener(manual)
        self.editor = Editor(manual)
        self.writer = Writer(manual)

    def work(self):
        today = datetime.now()
        logging.debug('[MANAGER] work at {}.'.format(today.strftime('%Y-%m-%d')))

        # Main loop.
        while True:
            start = time.perf_counter()
            now_time = datetime.now()
            # Listen.
            talking = self.listener.work()
            # Edit.
            self.editor.work(talking, now_time)

            # Writer interval.
            if now_time.day - today.day == self.manual.write_interval:
                logging.info('[MANAGER] write at:{}'.format(today.strftime('%Y-%m-%d')))
                # Refresh Edit.
                diary = self.editor.off_work(now_time)
                # Write.
                self.writer.work(diary)
                today = now_time

            # Listener interval. (Blocking the main process)
            time.sleep(max(0, self.manual.listen_interval - (time.perf_counter() - start)))
