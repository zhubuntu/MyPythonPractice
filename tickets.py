# coding: utf-8

"""�����л�Ʊ�鿴��

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   ��ʾ�����˵�
    -g          ����
    -d          ����
    -t          �ؿ�
    -k          ����
    -z          ֱ��

Example:
    tickets ���� �Ϻ� 2016-10-10
    tickets -dg �ɶ� �Ͼ� 2016-10-10
"""
from docopt import docopt

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    print(arguments)

if __name__ == '__main__':
    cli()