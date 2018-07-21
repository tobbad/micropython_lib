# -*- coding: utf-8 -*-
#
# (C) 2017 Tobias Badertscher <info@baerospace.ch>
#
# SPDX-License-Identifier:    BSD-3-Clause

import json
import logging

class SerDes:

    __REQ_ID=0

    def __init__(self, version=2):
        self._log = logging.getLogger("SerDes")
        if version not in (1,2):
            self._log.error("Only support JSON version 1 or 2")
            raise ValueError("Only support JSON version 1 or 2")
        self._ver = version
        self._log.debug("Created Version %d.0 JSON SerDes" % self._ver)

    def data_to_req(self, data):
        if data is None or len(data)==0:
            return None,  None,  None
        try:
            res = json.loads(data)
        except ValueError:
            self._log.error("ValueError")
            return None,  None,  None
        if self._ver==2:
            if not 'jsonrpc' in res:
                return None,  None,  None
            if res['jsonrpc'] != "2.0":
                return None,  None,  None
        if not 'method' in res:
            return None,  None,  None
        if not isinstance(res['method'], str):
            return None,  None,  None
        if not 'id' in res:
            res['id']="Null"
        if 'params' not in res:
            res['params']=None
        return res['id'], res['method'], res['params']

    def data_to_resp(self, data):
        if data is None or len(data)==0:
            return None,  None,  None
        try:
            res = json.loads(data)
        except ValueError:
            return None,  None,  None
        # id is always required
        if not 'id' in res:
            return None,  None,  None
        if self._ver == 2:
            # jsonrpc is required and version must be 2.0
            if not 'jsonrpc' in res:
                return None,  None,  None
            if  res['jsonrpc'] != "2.0":
                return None,  None,  None
            # Only one propertie should be there
            if 'result' in res and 'error' in res:
                return None,  None,  None
            # One must be there
            if not ('result' in res or 'error' in res):
                return None,  None,  None
            if 'result' in res:
                res['error']=None
            else:
                res['result']=None
        if self._ver == 1:
            # Both result and error must exist
            if not 'result' in res:
                return None,  None,  None
            if not 'error' in res:
                return None,  None,  None
            # Not both are allowed to be None
            if res['result'] is None and res['error'] is None:
                return None,  None,  None
            # Not both are allowed to be not None
            if res['result'] is not None and res['error'] is not None:
                return None,  None,  None
        return res['id'], res['result'], res['error']

    def req_to_data(self, methodName, params=None):
        req_id = self.__REQ_ID
        self.__REQ_ID += 1
        if isinstance(params, (int, float, str)):
            params=[params,]
        params = list() if params is None else list(params)
        data={"id":req_id ,
              "method":methodName,
              'params':params}
        if self._ver == 2:
            data["jsonrpc"] = "2.0"
        return req_id, json.dumps(data)

    def resp_to_data(self, req_id, result=None, error=None):
        data={"id":req_id }
        if self._ver == 2:
            data["jsonrpc"] = "2.0"
        if (result is not None) and error is not None:
            return None
        if (result is None) and error is None:
            return None
        if result is not None:
            data['result']=result
            data['error']= None
        else:
            if not isinstance(error, dict):
                return None
            if 'code' not in error:
                return None
            data['result']=None
            data['error']=error
        return json.dumps(data)
