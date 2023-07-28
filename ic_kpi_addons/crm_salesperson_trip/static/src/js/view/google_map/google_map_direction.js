odoo.define('crm_salesperson_trip.GoogleMapDirection', function (require) {
    'use strict';

    const core = require('web.core');
    const Widget = require('web.Widget');

    const _t = core._t;

    const GoogleMapDirection = Widget.extend({
        template: 'GoogleMapView.WaypointDirection',
        events: {
            'click button#submit': 'onButtonSubmitRoute',
            'click button#print': 'onButtonPrint',
            'change select#start': 'onChangeSelectStart',
            'change select#end': 'onChangeSelectEnd',
            'change select#waypoints': 'onChangeSelectWaypoint',
        },
        init: function (parent, waypoints, direction_panel) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.waypoints = waypoints;
            this.origin = null;
            this.destination = null;
            this.$directionPanel = direction_panel;
        },
        start: async function () {
            const _super = await this._super.apply(this, arguments);
            this.parent.$('.o_map_right_sidebar').toggleClass('open').toggleClass('closed');
            this.initializeDirection();
            return _super;
        },
        initializeDirection: function () {
            this.directionsService = new google.maps.DirectionsService();
            this.directionsRenderer = new google.maps.DirectionsRenderer({
                map: this.parent.gmap,
                draggable: true,
                panel: this.$directionPanel.get(0),
            });

            this.markerInfo = new google.maps.InfoWindow();
        },
        getData: function () {
            const data = [];
            let display_name;
            this.waypoints.forEach((record) => {
                display_name = this.getDisplayName(record);
                data.push({
                    id: record.data.id,
                    name: display_name,
                    latitude: record.data[this.parent.fieldLat],
                    longitude: record.data[this.parent.fieldLng],
                });
            });
            return data;
        },
        getDisplayName: function (record) {
            let default_display_name = 'Unknown display_name';
            if (Object.prototype.hasOwnProperty.call(record.data, 'display_name')) {
                default_display_name = record.data.display_name;
            } else if (Object.prototype.hasOwnProperty.call(record.data, 'name')) {
                default_display_name = record.data.name;
            } else if (Object.prototype.hasOwnProperty.call(record.fields, 'display_name')) {
                const display_name_field =
                    record.fields['display_name'].depends.length > 0 ? record.fields['display_name'].depends[0] : false;
                if (display_name_field) {
                    try {
                        default_display_name = record.data[display_name_field].data.display_name;
                    } catch (error) {
                        console.warn(error);
                    }
                }
            }
            return default_display_name;
        },
        onButtonSubmitRoute: function () {
            let origin = this.origin ? this.origin.id : false;
            let destination = this.destination ? this.destination.id : false;

            if (!origin) {
                origin = parseInt(this.$('select#start').children('option:selected').val());
            }
            if (!destination) {
                destination = parseInt(this.$('select#end').children('option:selected').val());
            }

            if (!origin || !destination) {
                this.do_notify('Warning', _t('Please select at least location start and location end'));
                return;
            }

            this.$('button#print').prop('disabled', false);

            const reserved_points = [origin, destination];
            const reserved_points_ids = reserved_points;
            const waypoints = [];
            if (this.selectedWaypoints) {
                this.selectedWaypoints.forEach((record) => {
                    if (reserved_points.indexOf(record.id) === -1) {
                        waypoints.push(record);
                        reserved_points_ids.push(record.id);
                    }
                });
            }
            this.setWaypointResult(waypoints);
            if (!this.parent.$('.o_map_right_sidebar').hasClass('open')) {
                this.parent.$('.o_map_right_sidebar').toggleClass('open').toggleClass('closed');
            }

            this.parent.markers.forEach((marker) => {
                if (reserved_points_ids.indexOf(marker._odooRecord.res_id) === -1) {
                    marker.setMap(null);
                } else {
                    marker.setMap(this.parent.gmap);
                }
            });

            if (!this.parent.$('.o_map_right_sidebar').hasClass('open')) {
                this.parent.$('.o_map_right_sidebar').toggleClass('open').toggleClass('closed');
            }

            this.setWaypointResult(waypoints);
        },
        onButtonPrint: function () {
            const direction = this.directionsRenderer.getDirections();
            if (direction) {
                this.parent.toggleSidebarleft();
                const bounds = direction.routes[0].bounds;
                this.parent.gmap.fitBounds(bounds);
                google.maps.event.addListenerOnce(this.parent.gmap, 'idle', () => {
                    google.maps.event.trigger(this.parent.gmap, 'resize');
                    setTimeout(() => {
                        window.print();
                    }, 500);
                });
            }
        },
        onChangeSelectStart: function (ev) {
            const origin = {};
            const $optSelected = $(ev.currentTarget).children('option:selected');
            if ($optSelected.index() > -1) {
                origin.id = parseInt($optSelected.val());
                origin.lat = $optSelected.data('lat');
                origin.lng = $optSelected.data('lng');
            }
            this.origin = origin;
        },
        onChangeSelectEnd: function (ev) {
            const dest = {};
            const $optSelected = $(ev.currentTarget).children('option:selected');
            if ($optSelected.index() > -1) {
                dest.id = parseInt($optSelected.val());
                dest.lat = $optSelected.data('lat');
                dest.lng = $optSelected.data('lng');
            }
            this.destination = dest;
        },
        onChangeSelectWaypoint: function (ev) {
            const waypts = [];
            $(ev.currentTarget)
                .find('option:selected')
                .each(function () {
                    const $target = $(this);
                    waypts.push({
                        id: parseInt($target.val()),
                        name: $target.text(),
                        latitude: $target.data('lat'),
                        longitude: $target.data('lng'),
                    });
                });
            this.selectedWaypoints = waypts;
        },
        setWaypointResult: function (waypoints) {
            if (Object.keys(this.origin).length === 0 || Object.keys(this.destination).length === 0) {
                this.do_warn('No direction given');
            } else {
                const origin = this.origin;
                delete origin.id;
                const destination = this.destination;
                delete destination.id;

                const waypoints_selected = _.map(waypoints, (point) => ({
                    location: {
                        lat: point.latitude,
                        lng: point.longitude,
                    },
                    stopover: true,
                }));

                setTimeout(() => {
                    this.directionsService
                        .route({
                            origin: origin,
                            destination: destination,
                            waypoints: waypoints_selected,
                            travelMode: google.maps.TravelMode.DRIVING,
                            avoidTolls: true,
                        })
                        .then((result) => {
                            this.directionsRenderer.setDirections(result);
                        })
                        .catch((error) => {
                            this.do_warn('Directions request failed due to ' + error);
                        });
                }, 1000);
            }
        },
    });

    return GoogleMapDirection;
});
