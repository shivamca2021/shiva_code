odoo.define('web.search_wizard', function(require){
"use strict";
var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var AbstractWebClient = require('web.AbstractWebClient');

var logwizard = Widget.extend({
    template: 'logwizard',
    events: {
        'click': '_onClick',
    },

    _onClick(ev) {
        var url = window.location.href;
        ev.preventDefault();

//        {

        this.do_action({

                    name: ' ',
                    type: 'ir.actions.act_window',
                    res_model: 'log.custom',
                    target: 'new',
                    views: [[false, 'form']],
                    context: {'alert_url':url}
                });

//        }
    }
});

//
SystrayMenu.Items.push(logwizard);
return logwizard;
});