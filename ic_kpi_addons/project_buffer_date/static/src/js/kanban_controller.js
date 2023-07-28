odoo.define('project_buffer_date.kanban_controller', function (require) {
"use strict";

const KanbanController = require('web.KanbanController');

var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if(this.$buttons){
                this.$buttons.on('click', 'button.o-kanban-button-edit-project', this._editProject.bind(this));
            }

        },
        _editProject: function () {
	        var state = this.model.get(this.handle, {raw: true});
	        this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'project.project',
                views: [[this.formViewId || false, 'form']],
                res_id: state.context.default_project_id,
                target: 'current',
                context: {'form_view_initial_mode': 'edit'},
            });

	    },

 };

 KanbanController.include(includeDict);


});
