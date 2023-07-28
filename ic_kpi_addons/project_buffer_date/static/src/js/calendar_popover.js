odoo.define('project_buffer_date.calendar_popover', function (require) {
"use strict";

const CalendarRenderer = require('web.CalendarRenderer');
const CalendarPopover = require('web.CalendarPopover');
const session = require('web.session');


const BufferCalendarPopover = CalendarPopover.include({
    
    /**
     * @constructor
     */
    init: function () {
        var self = this;
        this._super.apply(this, arguments);
    },

    
    /**
     * @override
     * @return {boolean}
     */
    isEventDeletable() {
        return this.modelName == 'project.task.stage' ? false : this._super();
    },
   
    /**
     * @override
     * @return {boolean}
     */
    isEventEditable() {
    	console.log(this.modelName);
        return this.modelName == 'project.task.stage' ? false : this._super();
    },
     

   
});


return BufferCalendarPopover

});
