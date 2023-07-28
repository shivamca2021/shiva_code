odoo.define('backend_theme_extension.Sidebar', function(require) {
    "use strict";
    var session = require('web.session');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    const AppsMenu = require("web.AppsMenu");
    AppsMenu.include({
        events: _.extend(
            {
                'click .o_appss': '_onAppsssMenuItemClicked',
                'click .star_icon_fun': '_RemoveFavApps',
                "click .menu_item_list_wrp .active": "_AddFavApps",
            },
            AppsMenu.prototype.events
        ),
        /**
         * @override
         * @param {web.Widget} parent
         * @param {Object} menuData
         * @param {Object[]} menuData.children
         */
        init: function (parent, menuData) {
            this._super.apply(this, arguments);
            this._activeApp = undefined;
            this._apps = _.map(menuData.children, function (appMenuData) {
                return {
                    actionID: parseInt(appMenuData.action.split(',')[1]),
                    menuID: appMenuData.id,
                    name: appMenuData.name,
                    xmlID: appMenuData.xmlid,
                    web_icon: appMenuData.web_icon,
                    web_icon_data: appMenuData.web_icon_data
                };
            });
        },
        _AddFavApps: async function(ev) {
            ev.preventDefault();
            const result = await this._rpc({
                route: "/backend_theme_extension/set_fav_icons",
                params: {
                    backend_app_id: $(ev.currentTarget).attr(
                        "data-menu-id"
                    ),
                },
            });
            if (result) {
                this.trigger_up("backend_update_fav_icon");
                $(ev.currentTarget).removeClass("active");
                this._ShowFavApps(ev);
            }
        },
        _RemoveFavApps: async function(ev) {
            ev.preventDefault();
            const result = await this._rpc({
                route: "/backend_theme_extension/rmv_fav_icons",
                params: {
                    backend_app_id: $(ev.currentTarget).attr(
                        "data-menu-id"
                    ),
                },
            });
            if (result) {
                this.trigger_up("backend_update_fav_icon");
                $(ev.currentTarget).addClass("active");
                this._ShowFavApps(ev);
            }
        },
        _ShowFavApps: async function(ev) {
            ajax.jsonRpc('/backend_theme_extension/show_all_fav_icon','call',{}).then(function(result) {
                $(".fav_all_icon_list").empty();
                $(".fav_all_icon_list").append(result);
            });
        },
        _onAppsssMenuItemClicked: function (ev) {
            ev.stopPropagation();
            var $target = $(ev.currentTarget);
            var menuID = $target.data('menu-id');
            var app = _.findWhere(this._apps, {menuID: menuID });
            this._openApp(app);
        },
        _openApp: function (app) {
            this._setActiveApp(app);
            if (!app) {
                return false
            }else{
                this.trigger_up('app_clicked', {
                    action_id: app.actionID,
                    menu_id: app.menuID,
                });
            }
        },
        _setActiveApp: function (app) {
            if (!app) {
                swal("Permission Denied!", "These options are not included in your system, please contact your system administrator or sales@ic-kpi.com to explore adding additional modules.", "success");
            } else {
                var $oldActiveApp = this.$('.o_app.active');
                $oldActiveApp.removeClass('active');
                var $newActiveApp = this.$('.o_app[data-action-id="' + app.actionID + '"]');
                $newActiveApp.addClass('active');
            }
        },
    });
    $(function() {
        $("#sidebar a").each(function() {
            var url = $(this).attr('href');
            if (session.debug == 1) $(this).attr('href', $.addDebug(url));
            if (session.debug == 'assets') $(this).attr('href', $.addDebugWithAssets(url));
            if (session.debug == false) $(this).attr('href', $.delDebug(url));
        });
        setTimeout(function(){
            $(".full").click(function(ev) {
                ev.preventDefault();
                $('ul.o_menu_apps li div.dropdown-menu .o_app').removeClass('o_hidden');
                $('ul.o_menu_apps li div.dropdown-menu .our_apps').addClass('o_hidden');
                if($("#sidebar li").hasClass('active_sidebar')){
                    setTimeout(function(){
                        $(".full").trigger('click');
                    },100);
                }
                $("#sidebar li").removeClass('active_sidebar');
                $(this).addClass('active_sidebar');
            });
        },500);
        $("#sidebar li").click(function(ev) {
            ev.stopPropagation();
            $(".full").removeClass('active_sidebar');
            $("#sidebar li").removeClass('active_sidebar');
            $(this).addClass('active_sidebar');
            var s_name = $(this).find('img').attr('title')
            ajax.jsonRpc("/submenu/dashboard", 'call', {
                'menu_name' : s_name,
                }).then(function (res){
                    $('.our_apps').empty().html(res)
                   if (!res){
                        swal("Permission Denied!", "These options are not included in your system, please contact your system administrator or sales@ic-kpi.com to explore adding additional modules.", "success");
                    }
                    if(!$('ul.o_menu_apps li').hasClass('show')){
                        $('ul.o_menu_apps li').addClass('show');
                    }
                    if(!$('ul.o_menu_apps li div.dropdown-menu').hasClass('show')){
                        $('ul.o_menu_apps li div.dropdown-menu').addClass('show');
                    }
                    $('ul.o_menu_apps li div.dropdown-menu .o_app').addClass('o_hidden');
                    $('ul.o_menu_apps li div.dropdown-menu .our_apps').removeClass('o_hidden');
                    $('ul.o_menu_apps li div.dropdown-menu .star_icon_fun').each(function(){
                        var star = $(this);
                        var start_data_menu = $(this).attr('data-menu-id');
                        var app_data_menu = $(this).parent().find('.o_appss').attr('data-menu-id');
                        rpc.query({
                            model: 'ir.ui.menu',
                            method: 'get_fav_menu',
                            args: [start_data_menu],
                        }).then(function (result) {
                            if(result == false){
                                $(star).addClass('active');
                            }
                        });
                    });
                });
            });
    });
});
