odoo.define('crm_salesperson_trip.GoogleMapRenderer', function (require) {
    'use strict';

    const viewRegistry = require('web.view_registry');
    const GoogleMapRenderer = require('web_google_maps.GoogleMapRenderer').GoogleMapRenderer;
    const GoogleMapView = require('web_google_maps.GoogleMapView');
    const GoogleMapDirection = require('crm_salesperson_trip.GoogleMapDirection');

    const GoogleMapDirectionRenderer = GoogleMapRenderer.extend({
        template: 'GoogleMapView.MapViewRouteDirection',
        events: _.extend({}, GoogleMapRenderer.prototype.events, {
            'click .toggle_left_sidebar': 'onToggleLeftSidebar',
        }),
        start: function () {
            const self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_map_right_sidebar').addClass('route');
            });
        },
        _renderSidebar: function () {
            if (!this.widgetMapDirection) {
                const directionPanel = this.$('.o_map_right_sidebar').find('.content');
                this.widgetMapDirection = new GoogleMapDirection(this, this.state.data, directionPanel);
                const $leftSidebar = this.$('.o_map_left_sidebar');
                this.widgetMapDirection.appendTo($leftSidebar);
            }
        },
        onToggleLeftSidebar: function (ev) {
            ev.preventDefault();
            this.toggleSidebarleft();
        },
        toggleSidebarleft: function () {
            this.$('.o_map_left_sidebar').toggleClass('closed').toggleClass('opened');
            this.$('.o_map_left_sidebar').find('.toggle_left_sidebar > button').toggleClass('closed');
        }
    });

    const GoogleMapDirectionView = GoogleMapView.extend({
        config: _.extend({}, GoogleMapView.prototype.config, {
            Renderer: GoogleMapDirectionRenderer,
        }),
    });

    viewRegistry.add('google_map_route_direction', GoogleMapDirectionView);
});
