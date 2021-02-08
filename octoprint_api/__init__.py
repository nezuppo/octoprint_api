#!/usr/bin/env python3

import json
import urllib.request
import time

class OctoPrintRest:
    def __init__(self, apikey_file, server=None, port=None):
        if not server:
            server = 'localhost'
        if not port:
            port = 5000

        self.__url_base = 'http://{}:{}'.format(server, port)
        with open(apikey_file) as f:
            self.__apikey = f.read().strip()

    def post(self, path, **kwargs):
        assert path.startswith('/'), path
        url = self.__url_base + path

        json_data = json.dumps(kwargs).encode('utf-8')
        req = urllib.request.Request(url)
        req.add_header('X-Api-Key', self.__apikey)
        req.add_header('Content-Type', 'application/json')
        req.data = json_data

        with urllib.request.urlopen(req) as f:
            ret_json = f.read().decode()

        assert ret_json == '', ret_json

    def get(self, path):
        assert path.startswith('/'), path
        url = self.__url_base + path

        req = urllib.request.Request(url)
        req.add_header('X-Api-Key', self.__apikey)

        with urllib.request.urlopen(req) as f:
            ret_json = f.read().decode()
        
        return json.loads(ret_json)

class OctoPrint(OctoPrintRest):
    def __init__(self, apikey_file, server=None, port=None):
        super().__init__(apikey_file, server, port)

    def jog(self, x=None, y=None, z=None, absolute=True):
        absolute = True if absolute else False
        xyz_milli = {}

        if x is not None: xyz_milli['x'] = x / 1000
        if y is not None: xyz_milli['y'] = y / 1000
        if z is not None: xyz_milli['z'] = z / 1000

        if xyz_milli == {}:
            raise Exception()

        self.post('/api/printer/printhead', command='jog', absolute=absolute, **xyz_milli)

    def check_connection(self):
        ret = self.get('/api/connection')
        assert ret['current']['state'] == 'Operational', ret['current']['state']

    def connect_w(self):
        self.post('/api/connection', command='connect', baudrate=250000)
        for i in range(15):
            ret = self.get('/api/connection')
            if ret['current']['state'] == 'Operational':
                break
            time.sleep(1)
        else:
            raise Exception()

    def disconnect_w(self):
        self.post('/api/connection', command='disconnect')
        for i in range(15):
            ret = self.get('/api/connection')
            if ret['current']['state'] == 'Closed':
                break
            time.sleep(1)
        else:
            raise Exception(ret)
