from argparse import ArgumentParser

from items.manual import Manual
from workers.manager import Manager


def main():
    parser = ArgumentParser()
    parser.add_argument('--diary-path', help='The diary saved path', default='C:/ServerDiary/diary')
    parser.add_argument('--report-path', help='The report saved path. (not use now)', default='C:/ServerDiary/report')
    parser.add_argument('--write-interval', help='The interval between writing a story, in days.', default=1)
    parser.add_argument('--listen-interval', help='The interval between listening to a story, in seconds.', default=60)
    parser.add_argument('--listened-status', help='The status of listened process.', default=['running'])
    parser.add_argument('--mem-threshold', help='Memory threshold. (percent)', default=10)
    parser.add_argument('--cpu-threshold', help='CPU threshold. (percent)', default=1)
    parser.add_argument('--debug', help='Debug model, log in console.', default=True)
    args = parser.parse_args()

    manual = Manual(
        diary_path=args.diary_path,
        report_path=args.report_path,
        write_interval=args.write_interval,
        listened_status=args.listened_status,
        mem_threshold=args.mem_threshold,
        cpu_threshold=args.cpu_threshold,
        listen_interval=args.listen_interval,
        debug=args.debug
    )
    manager = Manager(manual)
    manager.work()


if __name__ == '__main__':
    main()
