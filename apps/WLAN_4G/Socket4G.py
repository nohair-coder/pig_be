# coding: utf8
import ast
import socketserver
import threading
import time

from .HttpDB import dataPost, pigPost
from ..WLAN_4G import Handle4G

exit_flag = False
timer_cnt = 0
udp_server = 0

handle_num = 0
put_num = 0
json_num = 0


class MySocket(socketserver.BaseRequestHandler):

    def handle(self):
        global udp_server
        global handle_num
        global put_num
        try:
            handle_num += 1
            data = self.request[0].decode()
            Addr_4G = self.client_address
            udp_server = self.request[1]
            print('接收到的数据是--------->', data)
            if (data[0] == '$' and data[12] == '#' and len(data) == 13) or (data[0] == '{' and data[-1] == '}'):
                put_num += 1
                Handle4G.Recv_4G_Queue.put([data, Addr_4G])
            else:
                print('error Recv')
        except Exception as e:
            print(e)
            print(self.request[0].decode(), '*************************', self.client_address)


def Init_4GSocket():
    """4G Socket 初始化"""
    Send_4G_Thread = threading.Thread(target=Send_4G)
    Send_4G_Thread.start()
    server = socketserver.ThreadingUDPServer(('0.0.0.0', 8100), MySocket)
    server.serve_forever()


def Send_4G():
    """4G发送"""
    print(threading.current_thread().name, 'Send_4G is running...')
    while not exit_flag:
        send_msg = Handle4G.Send_4G_Queue.get(block=True)
        # data = send_msg[0].encode()
        data = send_msg[0].encode()
        udp_server.sendto(data, send_msg[1])
        time.sleep(0.1)


def Handle_4G():
    """处理命令"""
    global json_num
    print(threading.current_thread().name + 'running...')
    while not exit_flag:
        try:
            msg_addr = Handle4G.Recv_4G_Queue.get()
            msg = msg_addr[0]
            Addr_4G = msg_addr[1]
            if msg is not None:
                if msg[0] == '$' and msg[12] == '#' and len(msg) == 13:
                    data = Handle4G.getFunctionCode(msg)
                    func_code = data['func_code']
                    if func_code == Handle4G.FUN_CODE_DICT['heart_beat']:  # 00 心跳
                        print(msg)
                        Handle4G.network_management(msg, Addr_4G)
                    # elif data['func_code'] == Analysis_4G.FUN_CODE_DICT['close_device']:  # 01 关机
                    #     pass
                    # elif data['func_code'] == Analysis_4G.FUN_CODE_DICT['open_device']:  # 02 开机
                    #     pass
                    elif func_code == Handle4G.FUN_CODE_DICT['data_object_request']:  # 03开始接收数据
                        Handle4G.promiseRequest(msg, Addr_4G)
                    elif data['func_code'] == Handle4G.FUN_CODE_DICT['send_complete']:  # 05 接收数据完成
                        pass
                    elif func_code == Handle4G.FUN_CODE_DICT['sync_datetime']:  # 06 请求同步时间
                        Handle4G.syncTime(Addr_4G)
                    else:
                        print('Node', Handle4G.getFunctionCode(msg)['func_code'], ' can not identify !')
                else:
                    json_num += 1
                    Handle4G.dataAnalyse(ast.literal_eval(msg))
        except:
            pass


def serverSend():
    """上传数据"""
    print(threading.current_thread().name, 'serverSend is running...')
    while not exit_flag:
        try:
            data_obj = Handle4G.serverSendQueue.get(timeout=3)
            server_flag = 0
            if data_obj['func'] == 'intake':
                server_flag = dataPost(data_obj)
            elif data_obj['func'] == 'addpig':
                server_flag = pigPost(data_obj)
            elif data_obj['func'] == 'changestation':
                pass
            elif data_obj['func'] == 'changedata':
                pass
            # if not dataPost(data_obj):
            #     print('serverSend Error')
            # Analysis_4G.serverSendQueue.put(data_obj)
            time.sleep(0.1)
            if not server_flag:
                with open('../../error.txt', 'a') as fe:
                    fe.write(data_obj + '\n')
        except:
            pass


def timer():
    """定时任务"""
    global timer_cnt
    global handle_num
    global put_num
    global json_num
    while not exit_flag:
        timer_cnt += 1
        if timer_cnt > 100000:
            timer_cnt = 0
            print('handle_num', handle_num)
            print('put_num', put_num)
            print('json_num', json_num)
        if timer_cnt % 10 == 1:  # 每10秒调用一次
            Handle4G.nodeMonitor()
        if timer_cnt % 2 == 1:  # 每2秒调用一次
            Handle4G.timeoutHandler()
        time.sleep(1)


def setDeviceStatus(cmd):
    """设定测定站状态，[[nodeId,"open_device"],[nodeId,"close_device"]]"""
    try:
        for i in cmd:
            Handle4G.deviceStart(int(i[0]), i[1])
        return True
    except Exception as e:
        print(e)
        return False


def getDeviceStatus(nodeId):
    """获得测定站状态,返回["ON","00000"]获取一个"""
    try:
        not_exit_station_statue = {
            'work_status': 'OFF'
        }
        status = Handle4G.device_status.get(str(int(nodeId)), not_exit_station_statue)
        if status['work_status'] == 'OFF':
            res = ['OFF', '00000']
        elif status['work_status'] == 'ON':
            res = ['ON', '00000']
        else:
            res = ['ON', status['work_status']]
        return res
    except Exception as e:
        print('获取测定站状态失败 ----------------->>>')
        print(e)
        return False


socket_4G_thread = threading.Thread(target=Init_4GSocket)
socket_4G_thread.start()
Hand4GThread = threading.Thread(target=Handle_4G)
Hand4GThread.start()
serverSendThread = threading.Thread(target=serverSend)
serverSendThread.start()
timer_thread = threading.Thread(target=timer)
timer_thread.start()
