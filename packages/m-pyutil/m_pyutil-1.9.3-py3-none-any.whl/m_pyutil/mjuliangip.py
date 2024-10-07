import hashlib
import logging
import uuid
from enum import Enum
from sqlite3 import IntegrityError

import requests

from m_pyutil.mdate import add_secs, nowt
from m_pyutil.msqlite import create, select, save

DB_FILE = 'juliangip.db'


class ProxyProtocol(Enum):
    HTTP = '1'
    SOCKS = '2'


class DynamicIP:

    def __init__(self, api_key: str):
        self.api_key = api_key
        create(sql='create table if not exists t_ip(id integer primary key autoincrement, ip text, expire_time text, create_time text)',
               f=DB_FILE)
        create(sql='create table if not exists t_lock(id integer primary key autoincrement, uid text unique not null, lock_id text unique not null)',
               f=DB_FILE)

    def get_ips(self,
                trade_no: str,
                num: int = 1,
                protocol: ProxyProtocol = ProxyProtocol.HTTP,
                force: bool = False) -> list:
        ips = []
        if not force:
            now_time = add_secs(nowt(), 1)
            ips = select(sql='select ip from t_ip where expire_time >= ? limit ?',
                         params=[now_time, num],
                         f=DB_FILE)
            ips = [ip[0] for ip in ips]
            if len(ips) >= num:
                return ips

        uid = str(uuid.uuid4())
        try:
            save(sql='insert into t_lock(uid, lock_id) values(?, ?)',
                 params=[uid, 'get_ips'],
                 f=DB_FILE)
        except IntegrityError:
            return ips

        url = f'auth_type=2&auto_white=1&ip_remain=1&num={num}&pt={protocol.value}&result_type=json&trade_no={trade_no}&key={self.api_key}'
        url = f'{url}&sign={hashlib.md5(url.encode("utf-8")).hexdigest()}'
        url = f'http://v2.api.juliangip.com/company/dynamic/getips?{url}'
        res = requests.get(url)
        if res.status_code != 200:
            logging.warning(f'get ips failed: {res.status_code}')
            return ips
        res_json = res.json()
        code = res_json['code']
        if code != 200:
            logging.warning(f'get ips failed: {res_json}')
            return ips
        proxy_list = res_json['data']['proxy_list']

        for proxy in proxy_list:
            proxy = proxy.split(',')
            host_port = proxy[0]
            time_user_pwd = proxy[1].split(':')
            time = int(time_user_pwd[0])
            user = time_user_pwd[1]
            pwd = time_user_pwd[2]
            ip = f'{user}:{pwd}@{host_port}'
            save(sql='insert into t_ip(ip, expire_time, create_time) values(?, ?, ?)',
                 params=[ip, add_secs(nowt(), time), nowt()],
                 f=DB_FILE)
            ips.append(ip)

        save(sql='delete from t_lock where uid = ?',
             params=[uid],
             f=DB_FILE)

        return ips
