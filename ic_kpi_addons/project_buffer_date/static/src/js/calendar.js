odoo.define('project_buffer_date.calendar', function (require) {
    "use strict";
    var AbstractRenderer = require('web.AbstractRenderer');
    
    const CalendarRenderer = require('web.CalendarRenderer');
    var core = require('web.core');
	var _t = core._t;
	var qweb = core.qweb;
    
    CalendarRenderer.include({
    	_eventRender: function (event) {
    		 var render = this._super(...arguments);
    		 render = $(render);
    		 if(render.find('.red_class').length > 0){
    		 	render.addClass('o_cw_nobg');
    		 	render.addClass('exceed_class');
    		 }
    		 return render;
    	
	    },
    	
    	_getFullCalendarOptions: function () {
	        const oldOptions = this._super(...arguments);
	        const oldEventRender = oldOptions.eventRender;
	        oldOptions.eventRender = (info) => {
	        	var event = info.event;
	        	let element = $(info.el);
	            if (oldEventRender) {
	                oldEventRender.call(this.calendar, info);
	            }
	            if (this.model == 'project.task.stage') {
                    if (event.extendedProps.record.colorpicker){
                        element.find('.fc-bg').remove();
                        element.addClass('o_cw_nobg');
                        element.css({
                                    backgroundColor: event.extendedProps.record.colorpicker,
                                    color: 'white'
                                })
                    }

                    if(event.extendedProps.record.hide_on_calender){
                            return false;
                        }
                }
	         };
	        return oldOptions;
	    },
    
    });
    
    
});
