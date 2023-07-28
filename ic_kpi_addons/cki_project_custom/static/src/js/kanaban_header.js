odoo.define('cki_project_custom.KanbanColumn', function (require) {
    "use strict";
    var KanbanColumn = require('web.KanbanColumn');

    KanbanColumn.include({
        renderElement: function () {
           this._super();
           this.set_headers();
        },
        set_headers: function() {
            var self = this;
            var kanban_header_title = self.$('.o_kanban_header_title');
            var stage_id = kanban_header_title.parent().parent().data("id");
            var ids = self.id;
            if (this.modelName === 'project.task') {
	            this._rpc({
                model: 'project.task',
                method: 'get_stage_capacity',
                args: [{'stage_id':stage_id}],
	            }).then(function (values) {
	                 _.each(values, function (value) {
	                 	if (!kanban_header_title.parent().parent().hasClass( "o_column_folded" )){
	                 		var title = 'Stage Capacity (' + value +')';
	                    	kanban_header_title.find('span.o_column_title').after("<span class='o_column_title' title='"+title+"'>("+value+")</span>");
	                    }
	                });
	            });
	        }
            
        },
    });
});