# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import DataSet

class DataSet(DataSet):

    def do_search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None):
        """ Performs a search() followed by a read() (if needed) using the
        provided search criteria

        :param str model: the name of the model to search on
        :param fields: a list of the fields to return in the result records
        :type fields: [str]
        :param int offset: from which index should the results start being returned
        :param int limit: the maximum number of records to return
        :param list domain: the search domain for the query
        :param list sort: sorting directives
        :returns: A structure (dict) with two keys: ids (all the ids matching
                  the (domain, context) pair) and records (paginated records
                  matching fields selection set)
        :rtype: list
        """
        Model = request.env[model]
        ctx = dict(request.context)
        if domain:
            new_domain, started_list,ended_list, exist = [], [], [], False
            for line in domain:
                if '=ilike' in line:
                    new_domain.append([rec.replace('=ilike', 'ilike') for rec in line])
                    started_list.append(line)
                    exist =True
                elif 'like' in line:
                    new_domain.append([rec.replace('like', 'ilike') for rec in line])
                    ended_list.append(line)
                    exist = True
                else:
                    new_domain.append(line)
            if exist:
                ctx.update({'started_with': True, 'started': started_list, 'ended':ended_list})
                request.context = ctx
                domain = new_domain
        return Model.with_context(ctx).web_search_read(domain, fields, offset=offset, limit=limit, order=sort)