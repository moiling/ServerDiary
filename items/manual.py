import logging


class Manual:
    """
    The manual that defined how to help the server writing his diary.
    """

    def __init__(
            self,
            diary_path,             # The diary saved path.
            report_path,            # The report saved path. (not use now)
            write_interval=1,       # The interval between writing a story, in days.
            listened_status=None,   # The status of listened process.
            mem_threshold=10,       # If one user's all processes' memory and cpu uses under threshold,
            cpu_threshold=1,        # The user will be excepted. (inactive user)
            listen_interval=60,     # The interval between listening to a story, in seconds.
            debug=False             # Debug model, log in console.
    ):  # :)

        if listened_status is None:
            listened_status = ['running']

        self.diary_path = diary_path
        self.report_path = report_path
        self.write_interval = write_interval
        self.listened_status = listened_status
        self.mem_threshold = mem_threshold
        self.cpu_threshold = cpu_threshold
        self.listen_interval = listen_interval
        self.debug = debug
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
