# -*- coding: utf-8 -*-
import logging
import odoo
from odoo import http
from odoo.http import request, Response
from datetime import datetime, timedelta
import json
import ast
import datetime
from ..helper.utility import schema_validate
from ..helper.apis_schema import LOGIN, LOGOUT


class EMPLOGINAPI(odoo.http.Controller):

    @http.route('/api/v1/login', methods=['POST'], type='json', auth='public', website=True, csrf=False)
    def login(self, **post):
        print("-------------------------------------------------------------------------------------", post)
        print("post", post)
        _r = {}
        hr_employee_obj = request.env['hr.employee']
        post = request.jsonrequest
        msg = schema_validate(post, LOGIN)
        if msg:
            _r['status'] = 'Fail'
            _r['msg'] = msg
            _r['data'] = {}
            _r['code'] = 406
            return _r
        _un = post.get('username')
        _pw = post.get('password')
        employee = hr_employee_obj.verify_credentials(_un, _pw)
        if employee:
            _r['status'] = 'Pass'
            _r['msg'] = 'Employee logged-in successfully.'
            _r['code'] = 200
            _r['data'] = employee
            return _r
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Invalid username or password.'
            _r['data'] = {}
            _r['code'] = 200
        return _r

    @http.route('/api/v1/logout', methods=['POST'], type='json', auth='none')
    def logout(self, **post):
        _r = {}
        post = request.jsonrequest
        _r['status'] = 'Pass'
        _r['msg'] = 'You have been logged out successfully.'
        _r['data'] = {}
        _r['code'] = 200

        return _r
