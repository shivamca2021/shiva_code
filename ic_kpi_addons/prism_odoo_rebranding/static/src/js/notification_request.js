odoo.define('prism_odoo_rebranding/static/src/js/notification_request.js', function (require) {
  'use strict';

  const { patch } = require('web.utils');
  const components = {
    notification_request: require('mail/static/src/components/notification_request/notification_request.js')
  };

  patch(components.notification_request, 'prism_odoo_rebranding/static/src/js/notification_request.js', {
    _handleResponseNotificationPermission(value) {
        // manually force recompute because the permission is not in the store
        this.env.messaging.messagingMenu.update();
        if (value !== 'granted') {
            this.env.services['bus_service'].sendNotification(
                this.env._t("Permission denied"),
                this.env._t("Prism will not have the permission to send native notifications on this device.")
            );
        }
    }
  });
});