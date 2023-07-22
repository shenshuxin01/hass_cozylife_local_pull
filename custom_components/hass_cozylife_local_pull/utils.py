# -*- coding: utf-8 -*-
import json
import time
import requests
import logging

from custom_components.hass_cozylife_local_pull.ssx_test import get_local_get_pid_list

_LOGGER = logging.getLogger(__name__)


def get_sn() -> str:
    """
    message sn
    :return: str
    """
    return str(int(round(time.time() * 1000)))


# cache get_pid_list result for many calls
_CACHE_PID = []


class Res2:
    content = 1

    def __init__(self, content):
        self.content = content


def get_pid_list(lang='en') -> list:
    """
    http://doc.doit/project-12/doc-95/
    :param lang:
    :return:
    """
    global _CACHE_PID
    if len(_CACHE_PID) != 0:
        return _CACHE_PID

    res = Res2(1)
    try:
        _LOGGER.info('开始获取远程设备信息')
        raise ConnectionError
        domain = 'api-us.doiting.com'
        protocol = 'http'
        url_prefix = protocol + '://' + domain
        res = requests.get(url_prefix + '/api/device_product/model', {
            'lang': lang
        }, timeout=3)

        if 200 != res.status_code:
            _LOGGER.info('get_pid_list.result is none')
            return []
        _LOGGER.info('开始获取远程设备信息完成：res:')
        _LOGGER.info(res)
    except:
        _LOGGER.info('开始获取远程设备信息异常')
        res.content = get_local_get_pid_list()
        _LOGGER.info('开始获取远程设备信息异常信息res')
        _LOGGER.info(res)

    try:
        pid_list = json.loads(res.content)
    except:
        _LOGGER.info('get_pid_list.result is not json')
        return []

    if pid_list.get('ret') is None:
        return []

    if '1' != pid_list['ret']:
        return []

    if pid_list.get('info') is None or type(pid_list.get('info')) is not dict:
        return []

    if pid_list['info'].get('list') is None or type(pid_list['info']['list']) is not list:
        return []

    _CACHE_PID = pid_list['info']['list']
    return _CACHE_PID


if __name__ == '__main__':
    get_pid_list('en')
