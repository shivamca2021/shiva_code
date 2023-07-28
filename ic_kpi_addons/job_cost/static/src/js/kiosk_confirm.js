odoo.define('job_cost.kiosk_confirm', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var QWeb = core.qweb;
    
    
    var KioskConfirm = AbstractAction.extend({
        events: {
            "click .o_hr_attendance_back_button": function () { this.do_action(this.next_action, {clear_breadcrumbs: true}); },
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function () {
                var self = this;
                var mo_id = document.getElementById("mo_id").value;
                this._rpc({
                        model: 'hr.employee',
                        method: 'job_attendance_manual',
                        args: [[this.employee.id], 'job_cost.job_cost_attendance_action_my_attendances', mo_id],
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                        }
                    });
            }, 200, true),
            'click .o_hr_attendance_pin_pad_button_0': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 0); },
            'click .o_hr_attendance_pin_pad_button_1': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 1); },
            'click .o_hr_attendance_pin_pad_button_2': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 2); },
            'click .o_hr_attendance_pin_pad_button_3': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 3); },
            'click .o_hr_attendance_pin_pad_button_4': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 4); },
            'click .o_hr_attendance_pin_pad_button_5': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 5); },
            'click .o_hr_attendance_pin_pad_button_6': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 6); },
            'click .o_hr_attendance_pin_pad_button_7': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 7); },
            'click .o_hr_attendance_pin_pad_button_8': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 8); },
            'click .o_hr_attendance_pin_pad_button_9': function() { this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 9); },
            'click .o_hr_attendance_pin_pad_button_C': function() { this.$('.o_hr_attendance_PINbox').val(''); },
            'click .o_hr_attendance_pin_pad_button_ok': _.debounce(function() {
                var self = this;
                this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
                var mo_id = document.getElementById("mo_id").value;
                this._rpc({
                        model: 'hr.employee',
                        method: 'job_attendance_manual',
                        args: [[this.employee.id], 'job_cost.job_cost_attendance_action_my_attendances', this.workcenter_id, mo_id, this.$('.o_hr_attendance_PINbox').val()],
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                            self.$('.o_hr_attendance_PINbox').val('');
                            setTimeout( function() { self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled"); }, 500);
                        }
                    });
            }, 200, true),
        },
    
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.next_action = 'job_cost.job_cost_attendance_action_my_attendances';
            this.employee = action.employee_id;
            this.employee_name = action.employee_name;
            this.job_attendance_state = action.job_attendance_state;
            this.job_hours_today = field_utils.format.float_time(action.job_hours_today);
        },
        willStart: function () {
            var self = this;
    
            var def = this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    args: [[['id', '=', this.employee]], ['job_attendance_state', 'name', 'job_hours_today']],
                })
                .then(function (res) {
                    self.employee = res.length && res[0];
                    if (res.length) {
                        self.job_hours_today = field_utils.format.float_time(self.employee.job_hours_today);
                    }
                }); 
            var work = this._rpc({
                    model: 'mrp.workcenter',
                    method: 'get_workcenter',
                    args: [this.employee]
                })
                .then(function (wc_ids) {
                    self.wc_ids = wc_ids;
                }); 
            var mrp = this._rpc({
                    model: 'mrp.production',
                    method: 'get_manufacture_orders',
                    args: [this.employee]
                })
                .then(function (mo_ids) {
                    self.mo_ids = mo_ids;
                }); 
            return Promise.all([def, work, mrp, this._super.apply(this, arguments)]);
        },
    
        start: function () {
            var self = this;
            this.getSession().user_has_group('hr_attendance.group_hr_attendance_use_pin').then(function(has_group){
                self.use_pin = has_group;
                self.$el.html(QWeb.render("JobAttendanceMyMainMenu", {widget: self}));
                self.start_clock();
            });
            return self._super.apply(this, arguments);
        },
    
        start_clock: function () {
            this.clock_start = setInterval(function() {this.$(".o_hr_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));}, 500);
            // First clock refresh before interval to avoid delay
            this.$(".o_hr_attendance_clock").show().text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));
        },
    
        destroy: function () {
            clearInterval(this.clock_start);
            this._super.apply(this, arguments);
        },
    });
    
    core.action_registry.add('job_cost_kiosk_confirm', KioskConfirm);
    
    return KioskConfirm;
    
    });
    