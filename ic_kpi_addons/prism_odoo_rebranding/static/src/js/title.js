odoo.define('prism_odoo_rebranding.title', function (require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');
    var WebClient = require('web.AbstractWebClient');
    var AbstractController = require('web.AbstractController');
    var AbstractRenderer = require('web.AbstractRenderer');
    var CrashManager = require('web.CrashManager').CrashManager; // We can import crash_manager also
    var session = require('web.session');
    const { ComponentWrapper } = require('web.OwlCompatibility');
    var Widget = require('web.Widget');
    var ActionManager = require('web.ActionManager');
    var ErrorDialogRegistry = require('web.ErrorDialogRegistry');
//    var mail = require('mail.mail/static/src/components/notification_request/notification_request.js');

    var QWeb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;


    var map_title = {
        user_error: _lt('Warning'),
        warning: _lt('Warning'),
        access_error: _lt('Access Error'),
        missing_error: _lt('Missing Record'),
        validation_error: _lt('Validation Error'),
        except_orm: _lt('Global Business Error'),
        access_denied: _lt('Access Denied'),
    };
    $("input[name='website_domain']").attr("placeholder", "Domain");

//    mail.include({
//
//    _handleResponseNotificationPermission(value) {
//        // manually force recompute because the permission is not in the store
//        this.env.messaging.messagingMenu.update();
//        if (value !== 'granted') {
//            this.env.services['bus_service'].sendNotification(
//                this.env._t("Permission denied"),
//                this.env._t("Prism will not have the permission to send native notifications on this device.")
//            );
//        }
//    }
//
//    });

    AbstractRenderer.include({
        _renderNoContentHelper: function (context) {
        let templateName;
        if (!context && this.noContentHelp) {
            templateName = "web.ActionHelper";
            context = { noContentHelp: this.noContentHelp };
        } else {
            templateName = "web.NoContentHelper";
        }
        const template = document.createElement('template');
        // FIXME: retrieve owl qweb instance via the env set on Component s.t.
        // it also works in the tests (importing 'web.env' wouldn't). This
        // won't be necessary as soon as this will be written in owl.
        const owlQWeb = owl.Component.env.qweb;
        template.innerHTML = owlQWeb.renderToString(templateName, context);
        template.innerHTML = template.innerHTML.replace(/Odoo/g, 'Prism');
        $(template.content.firstChild).html($(template.content.firstChild).html().replace(/Odoo/g,'Prism'));
        this.el.append(template.content.firstChild);
    },
    });

    WebClient.include({
        init: function (parent) {
            this._super(parent);
            this.set('title_part', {"zopenerp": "Prism"});
            var obj = this;
            this._rpc({
            fields: ['company_name',],
            domain: [],
            model: 'website',
            method: 'search_read',
            limit: 1,
            context: session.user_context,
            })
            .then(function (result) {
                obj.set('title_part', {"zopenerp": result && result[0] && result[0].company_name || 'Prism'});  // Replacing the name 'Oodo' to selected company name near favicon
            });
        },
    });

    
window.addEventListener('unhandledrejection', ev =>
    core.bus.trigger('crash_manager_unhandledrejection', ev)
);

let active = true;

/**
 * An extension of Dialog Widget to render the warnings and errors on the website.
 * Extend it with your template of choice like ErrorDialog/WarningDialog
 */
var CrashManagerDialog = Dialog.extend({
    xmlDependencies: (Dialog.prototype.xmlDependencies || []).concat(
        ['/web/static/src/xml/crash_manager.xml']
    ),

    /**
     * @param {Object} error
     * @param {string} error.message    the message in Warning/Error Dialog
     * @param {string} error.traceback  the traceback in ErrorDialog
     *
     * @constructor
     */
    init: function (parent, options, error) {
        this._super.apply(this, [parent, options]);
        this.message = error.message;
        this.traceback = error.traceback;
        core.bus.off('close_dialogs', this);
    },
});

var ErrorDialog = CrashManagerDialog.extend({
    template: 'CrashManager.error',
});

var WarningDialog = CrashManagerDialog.extend({
    template: 'CrashManager.warning',

    /**
     * Sets size to medium by default.
     *
     * @override
     */
    init: function (parent, options, error) {
        this._super(parent, _.extend({
            size: 'medium',
       }, options), error);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Focuses the ok button.
     *
     * @override
     */
    open: function () {
        this._super({shouldFocusButtons: true});
    },
});

CrashManager.include({
 
    handleLostConnection: function () {
        var self = this;
        if (!this.isConnected) {
            // already handled, nothing to do.  This can happen when several
            // rpcs are done in parallel and fail because of a lost connection.
            return;
        }
        this.isConnected = false;
        var delay = 2000;
        core.bus.trigger('connection_lost');

        setTimeout(function checkConnection() {
            ajax.jsonRpc('/web/webclient/version_info', 'call', {}, {shadow:true}).then(function () {
                core.bus.trigger('connection_restored');
                self.isConnected = true;
            }).guardedCatch(function () {
                // exponential backoff, with some jitter
                delay = (delay * 1.5) + 500*Math.random();
                setTimeout(checkConnection, delay);
            });
        }, delay);
    },
    rpc_error: function(error) {
        error.message = error.message && error.message.replace("Odoo", "")
        // Some qunit tests produces errors before the DOM is set.
        // This produces an error loop as the modal/toast has no DOM to attach to.
        if (!document.body || !active || this.connection_lost) return;

        // Connection lost error
        if (error.code === -32098) {
            this.handleLostConnection();
            return;
        }

        // Special exception handlers, see crash_registry bellow
        var handler = core.crash_registry.get(error.data.name, true);
        if (handler) {
            new (handler)(this, error).display();
            return;
        }

        // Odoo custom exception: UserError, AccessError, ...
        if (_.has(this.odooExceptionTitleMap, error.data.name)) {
            error = _.extend({}, error, {
                data: _.extend({}, error.data, {
                    message: error.data.arguments[0],
                    title: this.odooExceptionTitleMap[error.data.name],
                }),
            });
            this.show_warning(error);
            return;
        }

        // Any other Python exception
        this.show_error(error);
    },
    show_warning: function (error, options) {
        if (!active) {
            return;
        }
        error.message = error.message && error.message.replace("Odoo", "")
        var message = error.data ? error.data.message : error.message;
        var title = _t("Something went wrong !");
        if (error.type) {
            title = _.str.capitalize(error.type);
        } else if (error.data && error.data.title) {
            title = _.str.capitalize(error.data.title);
        }
        return this._displayWarning(message, title, options);
    },
    show_error: function (error) {
        if (!active) {
            return;
        }
        error.message = error.message && error.message.replace("Odoo", "")
        error.traceback = error.data.debug;
        var dialogClass = error.data.context && ErrorDialogRegistry.get(error.data.context.exception_class) || ErrorDialog;
        var dialog = new dialogClass(this, {
            title: _.str.capitalize(error.type) || _t("Error"),
        }, error);


        // When the dialog opens, initialize the copy feature and destroy it when the dialog is closed
        var $clipboardBtn;
        var clipboard;
        dialog.opened(function () {
            // When the full traceback is shown, scroll it to the end (useful for better python error reporting)
            dialog.$(".o_error_detail").on("shown.bs.collapse", function (e) {
                e.target.scrollTop = e.target.scrollHeight;
            });

            $clipboardBtn = dialog.$(".o_clipboard_button");
            $clipboardBtn.tooltip({title: _t("Copied !"), trigger: "manual", placement: "left"});
            clipboard = new window.ClipboardJS($clipboardBtn[0], {
                text: function () {
                    return (_t("Error") + ":\n" + error.message + "\n\n" + error.data.debug).trim();
                },
               
                container: dialog.el,
            });
            clipboard.on("success", function (e) {
                _.defer(function () {
                    $clipboardBtn.tooltip("show");
                    _.delay(function () {
                        $clipboardBtn.tooltip("hide");
                    }, 800);
                });
            });
        });
        dialog.on("closed", this, function () {
            $clipboardBtn.tooltip('dispose');
            clipboard.destroy();
        });

        return dialog.open();
    },
    show_message: function(exception) {
        return this.show_error({
            type: _t("Client Error"),
            message: exception,
            data: {debug: ""}
        });
    },

    _displayWarning: function (message, title, options) {
        return new WarningDialog(this, Object.assign({}, options, {
            title,
        }), {
            message,
        }).open();
    },
});


var ExceptionHandler = {
    init: function(parent, error) {
    },
    display: function() {},
};

var RedirectWarningHandler = Widget.extend(ExceptionHandler, {  // Rewriting the exception handler
    init: function(parent, error) {
        this._super(parent);
        this.error = error;
    },
    display: function() {
        var self = this;
        var error = this.error;

        new WarningDialog(this, {
            title: _.str.capitalize(error.type) || _t("Warning"),   // Replacing 'Odoo Warning' to 'Warning'
            buttons: [
                {text: error.data.arguments[2], classes : "btn-primary", click: function() {
                    $.bbq.pushState({
                        'action': error.data.arguments[1],
                        'cids': $.bbq.getState().cids,
                    }, 2);
                    self.destroy();
                    location.reload();
                }},
                {text: _t("Cancel"), click: function() { self.destroy(); }, close: true}
            ]
        }, {
            message: error.data.arguments[0],
        }).open();
    }
});

core.crash_registry.add('odoo.exceptions.RedirectWarning', RedirectWarningHandler);


function session_expired(cm) {
    return {
        display: function () {   // Replace 'Odoo session expired' to 'Session Expired'
            cm.show_warning({type: _t("Session Expired"), data: {message: _t("Your Session expired. Please refresh the current web page.")}});
        }
    };
}
core.crash_registry.add('odoo.http.SessionExpiredException', session_expired);
    
    Dialog.include({
        init: function (parent, options) {
        var self = this;
        this._super(parent);
        this._opened = new Promise(function (resolve) {
            self._openedResolver = resolve;
        });
        if (this.on_attach_callback) {
            this._opened = this.opened(this.on_attach_callback);
        }
        options = _.defaults(options || {}, {
            title: _t('Prism'), subtitle: '',
            size: 'large',
            fullscreen: false,
            dialogClass: '',
            $content: false,
            buttons: [{text: _t("Ok"), close: true}],
            technical: true,
            $parentNode: false,
            backdrop: 'static',
            renderHeader: true,
            renderFooter: true,
            onForceClose: false,
        });
        this.$content = options.$content;
        this.title = options.title.replace("Odoo"," ");
        this.subtitle = options.subtitle.replace("Odoo"," ");
        this.fullscreen = options.fullscreen;
        this.dialogClass = options.dialogClass;
        this.size = options.size;
        this.buttons = options.buttons;
        this.technical = options.technical;
        this.$parentNode = options.$parentNode;
        this.backdrop = options.backdrop;
        this.renderHeader = options.renderHeader;
        this.renderFooter = options.renderFooter;
        this.onForceClose = options.onForceClose;

        core.bus.on('close_dialogs', this, this.destroy.bind(this));
    },
});
});

    

