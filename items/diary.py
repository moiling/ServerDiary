class Diary:
    """
    The diary struct.
    """
    def __init__(
            self,
            start_time=None,    # start listen time.
            end_time=None,      # end listen time.
            users=None,         # user info dist. info:{k=username, v=UseInfo}
    ):  # :)
        if users is None:
            users = {}

        self.users: {str, UseInfo} = users
        self.start_time = start_time
        self.end_time = end_time

    def page_turning(self):
        self.start_time, self.end_time, self.users = None, None, {}


class UseInfo:
    """
    Use information.
    """
    def __init__(
            self,
            cpu_use_history: list,  # cpu use percent in each listen time.
            mem_use_history: list,  # memory use percent in each listen time.
            date_history: list,     # date in each listen time.
            max_cpu_use,            # max cpu use percent.
            max_mem_use,            # max mem use percent.
            listen_count,           # listen count.
            use_time                # use server time.
    ):  # :)
        self.cpu_use_history = cpu_use_history
        self.mem_use_history = mem_use_history
        self.date_history = date_history
        self.max_cpu_use = max_cpu_use
        self.max_mem_use = max_mem_use
        self.listen_count = listen_count
        self.use_time = use_time
