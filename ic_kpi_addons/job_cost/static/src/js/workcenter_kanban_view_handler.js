
odoo.define('job_cost.workcenter_kanban_view_handler', function(require) {
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
            if (this.modelName === 'mrp.workcenter' && this.$el.parents('.o_job_cost_attendance_kanban').length) {
                                                // needed to diffentiate : check in/out kanban view of employees <-> standard employee kanban view
                var action = {
                    type: 'ir.actions.client',
                    name: 'Confirm',
                    tag: 'employee_kiosk_mode_job_cost',
                    workcenter_id: this.record.id.raw_value,
                };
                this.do_action(action);
            } else {
                this._super.apply(this, arguments);
            }
        }
    });
    
    });
