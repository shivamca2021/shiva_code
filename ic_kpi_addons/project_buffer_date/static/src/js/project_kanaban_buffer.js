odoo.define('project_buffer_date.KanbanColumn', function (require) {
    "use strict";
    var KanbanColumn = require('web.KanbanColumn');

    KanbanColumn.include({
        renderElement: function () {
           this._super();
           this.set_buffer_days();
        },
        set_buffer_days: function() {
            var self = this;
            var kanban_header_title = self.$('.o_kanban_header_title');
            var stage_id = kanban_header_title.parent().parent().data("id");
            var ids = self.id;
            var kanban_buffer_days = self.$('.o_kanban_counter_side');
            if (this.modelName === 'project.task') {
	            this._rpc({
                model: 'project.task',
                method: 'get_stage_buffer_days',
                args: [{'stage_id':stage_id}],
	            }).then(function (values) {
	                 _.each(values, function (value) {
	                 	if (!kanban_header_title.parent().parent().hasClass( "o_column_folded" )){
	                 		var title = 'Buffer Days';
	                    	self.$('.o_kanban_counter_side').prepend("<b class='o_column_title' title='"+title+"'>"+value+"</b></br>");
	                    }
	                });
	            });
	        }
            
        },
    });
});