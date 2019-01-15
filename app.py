import RPi.GPIO as GPIO

# see https://github.com/AllenSnape/Python-WebSocket
import WebSocket

import json
import time
import random
import socket
import threading

from bottle import static_file, route, run

host = socket.gethostname()
port = 80

# 计数
count = 0

# region 页面


@route('/')
@route('/index')
@route('/index.html')
def index():
    """ 主页 """
    return static_file('index.html', root='./')


@route('/reset')
def reset():
    """ 清空计数 """
    global count
    count = 0
    return json.dumps({'status': 200})


# endregion

# region WebSocket

ws = WebSocket.WebSocketServer(host, port + 1)
# 上一次推送时间: 最大推送时间限制在800ms内
last_publish_time = time.time()


def publish_counter():
    """ 使用ws推送计数 """
    data = json.dumps({'count': count, 'name': 'counter'})
    for _, ws_client in ws.get_clients().items():
        ws_client.send(data)


# endregion

# region GPIO操作

# 监听的GPIO针脚
pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 添加计数
def do_count(pin):
    global count, last_publish_time
    count += 1

    now = time.time()
    if now - last_publish_time >= .8:
        last_publish_time = now
        # 异步推送
        threading.Thread(target=publish_counter).start()

    print(count)


# TODO 模拟事件
def run_gpio():
    while True:
        time.sleep(random.random())
        do_count(pin)


# threading.Thread(target=run_gpio).start()


# endregion

try:
    # 添加监听器
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=do_count, bouncetime=100)
    # 异步启动ws
    threading.Thread(target=ws.run_forever).start()
    # 启动网页
    run(host=host, port=port)
finally:
    # 关闭ws
    ws.close()
    # 清除GPIO设置
    GPIO.remove_event_detect(do_count)
    GPIO.cleanup()
