odoo.define("backend_theme_extension.theme_appdrawer_edit", function (require) {
  "use strict";

  var Widget = require("web.Widget");
  var SystrayMenu = require("web.SystrayMenu");
  var ajax = require('web.ajax');
  var rpc = require('web.rpc');

  var BackendAppdrawerEdit = Widget.extend({
    template: "backend_appdrawer_edit",
    events: {
      "click #favorite_appdrawer": "_backendShowFavIcons",
    },
    init: function () {
      var self = this;
      this._super.apply(this, arguments);
    },
    _backendShowFavIcons: function (ev) {
       ev.preventDefault();
        ajax.jsonRpc('/backend_theme_extension/show_all_fav_icon','call',{}).then(function(result) {
            $(".fav_all_icon_list").empty();
            $(".fav_all_icon_list").append(result);
        });
    },
  });
  SystrayMenu.Items.push(BackendAppdrawerEdit);

  return {
    BackendAppdrawerEdit: BackendAppdrawerEdit,
  };
});
