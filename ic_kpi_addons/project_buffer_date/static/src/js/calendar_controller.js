odoo.define('project_buffer_date.calendar_controller', function (require) {
"use strict";

const CalendarController = require('web.CalendarController');
const CalendarView = require('web.CalendarView');
const viewRegistry = require('web.view_registry');
var QuickCreate = require('web.CalendarQuickCreate');
var core = require('web.core');
var _t = core._t;
var QWeb = core.qweb;

function dateToServer (date, fieldType) {
    date = date.clone().locale('en');
    if (fieldType === "date") {
        return date.local().format('YYYY-MM-DD');
    }
    return date.utc().format('YYYY-MM-DD HH:mm:ss');
}

const BufferCalendarController = CalendarController.include({

    _onOpenCreate: function (event) {
    	var self = this;
        if (["year", "month"].includes(this.model.get().scale)) {
            event.data.allDay = true;
        }
        var data = this.model.calendarEventToRecord(event.data);

        var context = _.extend({}, this.context, event.options && event.options.context);
        // context default has more priority in default_get so if data.name is false then it may
        // lead to error/warning while saving record in form view as name field can be required
        if (data.name) {
            context.default_name = data.name;
        }
        context['default_' + this.mapping.date_start] = data[this.mapping.date_start] || null;
        if (this.mapping.date_stop) {
            context['default_' + this.mapping.date_stop] = data[this.mapping.date_stop] || null;
        }
        if (this.mapping.date_delay) {
            context['default_' + this.mapping.date_delay] = data[this.mapping.date_delay] || null;
        }
        if (this.mapping.all_day) {
            context['default_' + this.mapping.all_day] = data[this.mapping.all_day] || null;
        }

        for (var k in context) {
            if (context[k] && context[k]._isAMomentObject) {
                context[k] = dateToServer(context[k]);
            }
        }

        var options = _.extend({}, this.options, event.options, {
            context: context,
            title: _.str.sprintf(_t('Create: %s'), (this.displayName || this.renderer.arch.attrs.string))
        });

        if (this.quick != null) {
            this.quick.destroy();
            this.quick = null;
        }

        if (!options.disableQuickCreate && !event.data.disableQuickCreate && this.quickAddPop) {
            this.quick = new QuickCreate(this, true, options, data, event.data);
            this.quick.open();
            this.quick.opened(function () {
                self.quick.focus();
            });
            return;
        }

        var title = _t("Create");
        if (this.renderer.arch.attrs.string) {
            title += ': ' + this.renderer.arch.attrs.string;
        }
        if (this.eventOpenPopup) {
            if (this.previousOpen) { this.previousOpen.close(); }
            this.previousOpen = new dialogs.FormViewDialog(self, {
                res_model: this.modelName,
                context: context,
                title: title,
                view_id: this.formViewId || false,
                disable_multiple_selection: true,
                on_saved: function () {
                    if (event.data.on_save) {
                        event.data.on_save();
                    }
                    self.reload();
                },
            });
            this.previousOpen.open();
        } else {
        	var m = this.modelName == 'project.task.stage' ? 'project.task' : this.modelName;
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: this.modelName == 'project.task.stage' ? 'project.task' : this.modelName,
                views: [[this.formViewId || false, 'form']],
                target: 'current',
                context: context,
            });
        }
    	
        },
    _onViewUpdated: function (event) {
            this.mode = event.data.mode;
            if (this.$buttons) {
                this.$buttons.find('.active').removeClass('active');
                this.$buttons.find('.o_calendar_button_' + this.mode).addClass('active');
            }
            const title = `${this.displayName} (${event.data.title})`;
            if(this.mode == 'week' && this.modelName == 'project.task.stage'){
                $('.fc-time-grid-container').css({'display':'none'});
                $('.fc-week').css({'height':'auto !important'});
            }
            
            return this.updateControlPanel({ title });
        },
});

const BufferCalendarView = CalendarView.extend({
        config: _.extend({}, CalendarView.prototype.config, {
            Controller: BufferCalendarController,
        }),
    });

    CalendarView.include({
        init: function () {
            this._super.apply(this, arguments);
            this.loadParams.eventLimit = 25;
        },
    });

    viewRegistry.add('calendar_controller', BufferCalendarView);
    return BufferCalendarView;
});
