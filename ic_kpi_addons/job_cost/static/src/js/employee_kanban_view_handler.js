
odoo.define('job_cost.employee_kanban_view_handler', function(require) {
    "use strict";
    
    var KanbanRecord = require('web.KanbanRecord');
    
    KanbanRecord.include({
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * @override
         * @private
         */
        _openRecord: function () {
            if (this.modelName === 'hr.employee.public' && this.$el.parents('.o_hr_employee_attendance_kanban_job_cost').length) {
                                                // needed to diffentiate : check in/out kanban view of employees <-> standard employee kanban view
                var action = {
                    type: 'ir.actions.client',
                    name: 'Confirm',
                    tag: 'job_cost_kiosk_confirm',
                    employee_id: this.record.id.raw_value,
                    employee_name: this.record.name.raw_value,
                    job_attendance_state: this.record.job_attendance_state.raw_value,
                    job_hours_today: this.record.job_hours_today.raw_value,
                };
                this.do_action(action);
            } else {
                this._super.apply(this, arguments);
            }
        }
    });
    
    });