odoo.define('backend_theme_extension.ActionManager', function (require) {
"use strict";

/**
 * The purpose of this file is to add the support of Odoo actions of type
 * 'ir_actions_account_report_download' to the ActionManager.
 */

var ActionManager = require('web.ActionManager');
var core = require('web.core');

ActionManager.include({

    /**
     * This is the entry point to execute Odoo actions, given as an ID in
     * database, an xml ID, a client action tag or an action descriptor.
     *
     * @param {number|string|Object} action the action to execute
     * @param {Object} [options]
     * @param {Object} [options.additional_context] additional context to be
     *   merged with the action's context.
     * @param {boolean} [options.clear_breadcrumbs=false] set to true to clear
     *   the breadcrumbs history list
     * @param {Function} [options.on_close] callback to be executed when the
     *   current action is active again (typically, if the new action is
     *   executed in target="new", on_close will be executed when the dialog is
     *   closed, if the current controller is still active)
     * @param {Function} [options.on_reverse_breadcrumb] callback to be executed
     *   whenever an anterior breadcrumb item is clicked on
     * @param {boolean} [options.pushState=true] set to false to prevent the
     *   ActionManager from pushing the state when the action is executed (this
     *   is useful when we come from a loadState())
     * @param {boolean} [options.replace_last_action=false] set to true to
     *   replace last part of the breadcrumbs with the action
     * @return {Promise<Object>} resolved with the action when the action is
     *   loaded and appended to the DOM ; rejected if the action can't be
     *   executed (e.g. if doAction has been called to execute another action
     *   before this one was complete).
     */
    doAction: function (action, options) {
        var self = this;
        options = _.defaults({}, options, {
            additional_context: {},
            clear_breadcrumbs: false,
            on_close: function () {},
            on_reverse_breadcrumb: function () {},
            pushState: true,
            replace_last_action: false,
        });

        // build or load an action descriptor for the given action
        var def;
        if (_.isString(action) && core.action_registry.contains(action)) {
            // action is a tag of a client action
            action = { type: 'ir.actions.client', tag: action };
        } else if (_.isNumber(action) || _.isString(action)) {
            // action is an id or xml id
            def = this._loadAction(action, {
                active_id: options.additional_context.active_id,
                active_ids: options.additional_context.active_ids,
                active_model: options.additional_context.active_model,
            }).then(function (result) {
                action = result;
            });
        }

        return this.dp.add(Promise.resolve(def)).then(function () {
            // action.target 'main' is equivalent to 'current' except that it
            // also clears the breadcrumbs
            if (!action){
            return false
            }
            options.clear_breadcrumbs = action.target === 'main' ||
                                        options.clear_breadcrumbs;

            self._preprocessAction(action, options);

            return self._handleAction(action, options).then(function () {
                // now that the action has been executed, force its 'pushState'
                // flag to 'true', as we don't want to prevent its controller
                // from pushing its state if it changes in the future
                action.pushState = true;

                return action;
            });
        }).then(function(action) {
            self.trigger_up('webclient_started');
            return action;
        });
    },

});

});