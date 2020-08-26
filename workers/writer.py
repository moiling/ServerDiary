import os

from items.manual import Manual
from items.diary import Diary


class Writer:
    """
    Someone who writing server's story.
    """

    def __init__(self, manual: Manual):
        """
        :param manual: The manual that defined how to help the server writing his diary.
                       Please see @manual.Manual
        """
        self.manual = manual

    def work(self, diary: Diary):
        """
        :param diary: diary to write.
        :return: None.
        """
        # output dir.
        summary_dir = os.path.join(self.manual.diary_path, diary.start_time.strftime('%Y-%m-%d'))
        user_info_dir = os.path.join(summary_dir, 'user info')
        # create output dir.
        os.makedirs(summary_dir, exist_ok=True)
        os.makedirs(user_info_dir, exist_ok=True)

        # write summary.
        summary_file = os.path.join(summary_dir, 'Summary.md')
        summary_fo = open(summary_file, 'w')
        summary_fo.write('# {}\n'.format(diary.start_time.strftime('%Y-%m-%d')))
        summary_fo.write('- Start time: {}\n'.format(diary.start_time.strftime('%Y-%m-%d %H:%M:%S')))
        summary_fo.write('- End time: {}\n'.format(diary.end_time.strftime('%Y-%m-%d %H:%M:%S')))

        summary_fo.write('|user|max cpu(%)|max memory(%)|use time(s)|\n|:-:|:-:|:-:|:-:|\n')
        for user, info in diary.users.items():
            name = user.split('\\')[-1]
            summary_fo.write('|{}|{:.2f}|{:.2f}|{}|\n'.format(name, info.max_cpu_use, info.max_mem_use, info.use_time))

            # write each user info.
            user_info_file = os.path.join(user_info_dir, '{}.md'.format(name))
            user_info_fo = open(user_info_file, 'w')

            user_info_fo.write('|cpu(%)|memory(%)|date|\n|:-:|:-:|:-:|\n')
            for i in range(len(info.cpu_use_history)):
                user_info_fo.write('|{:.2f}|{:.2f}|{}|\n'.format(
                    info.cpu_use_history[i],
                    info.mem_use_history[i],
                    info.date_history[i].strftime('%Y-%m-%d %H:%M:%S')
                ))

            user_info_fo.close()

        summary_fo.close()
