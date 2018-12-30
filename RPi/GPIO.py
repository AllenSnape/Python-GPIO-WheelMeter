# GPIO pin 编号方式
BOARD = 'BOARD'

# pin输出模式
IN = 1
OUT = 0

# pin默认状态
PUD_DOWN = 0
PUD_UP = 1

# pin监听状态
RISING = 1
FALLING = 0


def setmode(mode):
    """ 设置GPIO模式 """
    pass


def setup(pin, mode, pull_up_down=''):
    """ 设置pin """
    pass


def add_event_detect(pin, mode, callback=None, bouncetime=0):
    """ 监听pin输入值 """
    pass


def remove_event_detect(callback):
    """ 移除监听 """
    pass


def cleanup():
    """ 清楚设置 """
    pass
