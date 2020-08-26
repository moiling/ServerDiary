import time
import psutil
import logging
from items.manual import Manual


class Listener:
    """
    Someone who listening server's story.
    """

    def __init__(self, manual: Manual):
        """
        :param manual: The manual that defined how to help the server writing his diary.
                       Please see @manual.Manual
        """
        self.manual = manual

    def work(self):
        """
        Catch the memory and CPU use.
        :return: type: {dict{dict}}, info: {k=username, v={mem, cpu}}
        """
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        cpu_count = psutil.cpu_count()
        logging.debug('[LISTENER] cpu percent:{:.2f}%, cpu count:{}'.format(cpu_percent, cpu_count))

        for p in psutil.process_iter():
            p.cpu_percent(interval=None)  # last call.
        time.sleep(1)

        mem_per_users = {}  # memory percent per users. key is the user name.
        cpu_per_users = {}  # cpu percent per users of used cpu.
        for p in psutil.process_iter(['username', 'status', 'memory_percent']):
            if p.info['status'] not in self.manual.listened_status:
                continue
            if p.info['username'] is None:
                continue

            cpu = p.cpu_percent(interval=None)  # percentage since last call.
            if p.info['username'] in mem_per_users.keys():
                mem_per_users[p.info['username']] = mem_per_users[p.info['username']] + p.info['memory_percent']
                cpu_per_users[p.info['username']] = cpu_per_users[p.info['username']] + cpu
            else:
                mem_per_users[p.info['username']] = p.info['memory_percent']
                cpu_per_users[p.info['username']] = cpu

        user_info = {}
        for user in mem_per_users.keys():
            cpu_used = cpu_per_users[user] / cpu_count * cpu_percent / 100  # cpu percent per users of total cpu.
            mem_used = mem_per_users[user]
            # except idle users.
            if mem_used < self.manual.mem_threshold and cpu_used < self.manual.cpu_threshold:
                logging.debug('[LISTENER] idle user:{}, mem:{:.2f}%, cpu:{:.2f}%'.format(user, mem_used, cpu_used))
                continue

            user_info[user] = {'mem': mem_used, 'cpu': cpu_used}
            logging.debug('[LISTENER] active user:{}, mem:{:.2f}%, cpu:{:.2f}%'.format(user, mem_used, cpu_used))

        logging.debug('[LISTENER] return:{}'.format(user_info))
        return user_info


if __name__ == '__main__':
    m = Manual('', '', mem_threshold=20, cpu_threshold=1, debug=True)
    listener = Listener(m)
    talking = listener.work()
    print(talking)
