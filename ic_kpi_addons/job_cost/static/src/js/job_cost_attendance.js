odoo.define('job_cost.job_cost_attendance', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var field_utils = require('web.field_utils');
    
    
    var JobAttendances = AbstractAction.extend({
        contentTemplate: 'JobAttendanceMyMainMenu',
        events: {
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function() {
                this.update_attendance();
            }, 200, true),
        },
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
        },
    
        willStart: function () {
            var self = this;
    
            var def = this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    args: [[['user_id', '=', this.getSession().uid]], ['job_attendance_state', 'name', 'job_hours_today']],
                })
                .then(function (res) {
                    self.employee = res.length && res[0];
                    if (res.length) {
                        self.job_hours_today = field_utils.format.float_time(self.employee.job_hours_today);
                    }
                });
    
            return Promise.all([def, this._super.apply(this, arguments)]);
        },
    
        update_attendance: function () {
            var self = this;
            this._rpc({
                    model: 'hr.employee',
                    method: 'job_attendance_manual',
                    args: [[self.employee.id], 'job_cost.job_cost_attendance_action_my_attendances'],
                })
                .then(function(result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                    }
                });
        },
    });
    
    core.action_registry.add('job_cost_attendance_my_attendances', JobAttendances);
    
    return JobAttendances;
    
    });    