odoo.define('cki_project_custom.BasicView', function (require) {
"use strict";
var BasicView = require('web.BasicView');
var ajax = require('web.ajax');
BasicView.include({

        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            const model =  ['project.project','project.task'] ;
            if(model.includes(self.controllerParams.modelName)) {
                if(this.loadParams.context.uid){
                ajax.jsonRpc("/cki/project/archive", 'call', {
                        'uid': this.loadParams.context.uid
                    }).then(function(data){
                        if (data) {
                            console.log(">>>>>>>>>>>>>>>print datadatsa",data);
                            if(!data.access){
                                self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;
                            }
                         }
                    });
                 }
            }
        },
    });
});