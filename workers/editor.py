from items.manual import Manual
from items.diary import Diary, UseInfo
import copy


class Editor:
    """
    Someone who editing server's story. The origin talking needs editing before writing.
    """

    def __init__(self, manual: Manual):
        """
        :param manual: The manual that defined how to help the server writing his diary.
                       Please see @manual.Manual
        """
        self.manual = manual
        self.diary = Diary()

    def work(self, origin_talking, now):
        """
        :param origin_talking: type: {dict{dict}}, info: {k=username, v={mem, cpu}}
        :param now: time.
        :return: None. save in self.story.
        """
        if self.diary.start_time is None:
            self.diary.start_time = now

        for user, info in origin_talking.items():
            if user in self.diary.users.keys():
                use_info: UseInfo = self.diary.users[user]
                use_info.cpu_use_history.append(info['cpu'])
                use_info.mem_use_history.append(info['mem'])
                use_info.date_history.append(now)
                if info['cpu'] > use_info.max_cpu_use:
                    use_info.max_cpu_use = info['cpu']
                if info['mem'] > use_info.max_mem_use:
                    use_info.max_mem_use = info['mem']
                use_info.listen_count += 1
                use_info.use_time += self.manual.listen_interval
            else:
                # first meet this user.
                use_info = UseInfo(
                    cpu_use_history=[info['cpu']],
                    mem_use_history=[info['mem']],
                    date_history=[now],
                    max_cpu_use=info['cpu'],
                    max_mem_use=info['mem'],
                    listen_count=1,
                    use_time=self.manual.listen_interval
                )
                self.diary.users[user] = use_info

    def off_work(self, now):
        """
        Refresh.
        :param now: time.
        :return: dairy.
        """
        self.diary.end_time = now
        dairy = copy.deepcopy(self.diary)
        self.diary.page_turning()
        return dairy

