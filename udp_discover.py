import socket
import time
from .utils import get_sn
import logging


_LOGGER = logging.getLogger(__name__)

"""
discover device
"""


def get_ip() -> list:
    """
    get device ip
    :return: list
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind(('192.168.123.1', 0))
    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.1)
    socket.setdefaulttimeout(0.1)
    message = '{"cmd":0,"pv":0,"sn":"' + get_sn() + '","msg":{}}'
    
    i = 0
    while i < 3:
        # server.sendto(bytes(message, encoding='utf-8'), ('<broadcast>', 6095))
        server.sendto(bytes(message, encoding='utf-8'), ('255.255.255.255', 6095))
        # 使用mac的docker无法使用networkHost模式,扫描不到ip,所以使用下面手动配置ip
        server.sendto(bytes(message, encoding='utf-8'), ('192.168.0.10', 6095))
        time.sleep(0.03)
        server.sendto(bytes(message, encoding='utf-8'), ('192.168.0.12', 6095))
        time.sleep(0.03)
        i += 1

    # max tries before first data received
    max = 5
    i = 0
    while i < max:
        i += 1
        try:
            data, addr = server.recvfrom(1024, socket.MSG_PEEK)
        except Exception as err:
            _LOGGER.info(f'{i}/{max} try, udp timeout')
            continue
        _LOGGER.info(f'first udp.receiver:{addr[0]}')
        break
    else:
        _LOGGER.warning('cannot find any device')
        return []
    
    i = 255
    ip = []
    while i > 0:
        try:
            data, addr = server.recvfrom(1024)
        except:
            _LOGGER.info('udp timeout')
            break
        _LOGGER.info(f'udp.receiver:{addr[0]}')
        if addr[0] not in ip: ip.append(addr[0])
        i -= 1
    
    return ip
