# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore
from station import stations
import requests
init()
class TrainsCollection:

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, raw_train):
        duration = raw_train[10].replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for raw_trainS in self.available_trains:
            raw_train=raw_trainS.split('|')
            train_no = raw_train[3]
            initial = train_no[0].lower()
            newStation = {v: k for k, v in stations.items()}
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + newStation.get(str(raw_train[6])) + Fore.RESET,
                               Fore.RED + newStation.get(str(raw_train[7]))+ Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train[8] + Fore.RESET,
                            Fore.RED + raw_train[9] + Fore.RESET]),
                    self._get_duration(raw_train),
                    raw_train[31],  #一等
                    raw_train[30],  #二等
                    raw_train[23],  #软卧
                    raw_train[28],  #硬卧
                    raw_train[29],  #硬座
                    raw_train[26],   #无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
    # 添加verify=False参数不验证证书
    options = ''.join([
                          key for key, value in arguments.items() if value is True
                          ])
    r = requests.get(url, verify=False)
    available_trains = r.json()['data']['result']
    TrainsCollection(available_trains,options).pretty_print()

if __name__ == '__main__':
    cli()