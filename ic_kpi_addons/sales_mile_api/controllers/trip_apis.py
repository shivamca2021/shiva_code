# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import date, datetime, timedelta
from ..helper.utility import authenticate, schema_validate
from ..helper.apis_schema import *


class TRIPAPIS(http.Controller):

    def pre_check(self, data, schema):
        _r = {}
        valid = authenticate()
        if valid:
            return valid
        return False

    @http.route('/api/v1/trips', methods=['POST'], type='json', auth='user', csrf=False)
    def get_trips(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        user_id = post.get('user_id' or False) or False
        if not user_id:
            user_id = request.env.user.id
        trips = trip_obj.fetch_todays_trips(user_id)
        if trips:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trips fetched successfully.'
            _r['code'] = 201
            _r['data'] = trips
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = []
            _r['code'] = 200
        return _r

    @http.route('/api/v1/trip/detail', methods=['POST'], type='json', auth='user', csrf=False)
    def get_trip_detail(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        trip_id = post.get('trip_id')
        trip = trip_obj.get_trip_info(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trip info fetched successfully.'
            _r['code'] = 201
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = {}
            _r['code'] = 201
        return _r

    @http.route('/api/v1/leads/activity', methods=['POST'], type='json', auth='user', csrf=False)
    def leads_info(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, LEADS_ACTIVITY):
        #     return self.pre_check(post, LEADS_ACTIVITY)
        trip_id = post.get('trip_id')
        trip = trip_obj.get_leads_activity(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Lead Activity fetched successfully.'
            _r['code'] = 201
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = {}
            _r['code'] = 201
        return _r

    @http.route('/api/v1/leads/detail', methods=['POST'], type='json', auth='user', csrf=False)
    def get_leads_detail(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, LEADS_INFO):
        #     return self.pre_check(post, LEADS_INFO)
        trip_id = post.get('trip_id')
        trip = trip_obj.get_leads_info(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trip info fetched successfully.'
            _r['code'] = 201
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = {}
            _r['code'] = 201
        return _r

    @http.route('/api/v1/trip/start', methods=['POST'], type='json', auth='user', csrf=False)
    def start_trip(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        trip_id = post.get('trip_id')
        trip = trip_obj.start_trip(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trip started successfully.'
            _r['code'] = 202
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/complete', methods=['POST'], type='json', auth='user', csrf=False)
    def end_trip(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        trip_id = post.get('trip_id')
        trip = trip_obj.end_trip(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trip ended successfully.'
            _r['code'] = 202
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip does not exist.'
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/cancel', methods=['POST'], type='json', auth='user', csrf=False)
    def cancel_trip(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, TRIP_CANCEL):
        #     return self.pre_check(post, TRIP_CANCEL)
        trip_id = post.get('trip_id')
        trip = trip_obj.cancel_trip(trip_id)
        if trip:
            _r['status'] = 'Pass'
            _r['msg'] = 'Trip cancelled successfully.'
            _r['code'] = 202
            _r['data'] = trip
        else:
            _r['status'] = 'Fail'
            _r['msg'] = 'Trip Does not exist.'
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/meet/cancel', methods=['POST'], type='json', auth='user', csrf=False)
    def cancel_meet(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, MEETCANCEL):
        #     return self.pre_check(post, MEETCANCEL)
        trip_id = post.get('trip_id')
        customer_id = post.get('customer_id')
        _res = trip_obj.cancel_meet(trip_id, customer_id)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Meeting cancelled successfully.'
            _r['code'] = 202
            _r['data'] = _res
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/meet/reached', methods=['POST'], type='json', auth='user', csrf=False)
    def reached_meet(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, MEET_START_REACH):
        #     return self.pre_check(post, MEET_START_REACH)
        trip_id = post.get('trip_id')
        customer_d = post.get('customer_id')
        _res = trip_obj.reached_meet(trip_id, customer_d)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Meeting location reached successfully.'
            _r['code'] = 202
            _r['data'] = _res
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/meet/start', methods=['POST'], type='json', auth='user', csrf=False)
    def start_meet(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        trip_id = post.get('trip_id')
        customer_d = post.get('customer_id')
        _res = trip_obj.start_meet(trip_id, customer_d)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Meeting started successfully.'
            _r['code'] = 202
            _r['data'] = []
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/meet/complete', methods=['POST'], type='json', auth='user', csrf=False)
    def end_meet(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, MEETCOMPLETE):
        #     return self.pre_check(post, MEETCOMPLETE)
        _res = trip_obj.completed_meet(post)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Meeting completed successfully.'
            _r['code'] = 200
            _r['data'] = []
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/lead/location', methods=['POST'], type='json', auth='user', csrf=False)
    def location_update(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        # post = request.jsonrequest
        # if self.pre_check(post, MEETCOMPLETE):
        #     return self.pre_check(post, MEETCOMPLETE)
        _res = trip_obj.location_update(post)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Location Updated successfully.'
            _r['code'] = 200
            _r['data'] = _res
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r

    @http.route('/api/v1/trip/lead/location', methods=['POST'], type='json', auth='user', csrf=False)
    def location_update(self, **post):
        _r = {}
        trip_obj = request.env['crm.trip'].sudo()
        _res = trip_obj.location_update(post)
        if _res:
            _r['status'] = 'Pass'
            _r['msg'] = 'Location Updated successfully.'
            _r['code'] = 200
            _r['data'] = _res
        else:
            _r['status'] = 'Fail'
            _r['msg'] = _res
            _r['data'] = {}
            _r['code'] = 202
        return _r



