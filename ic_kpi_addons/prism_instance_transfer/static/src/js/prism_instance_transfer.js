odoo.define('prism_instance_transfer.TransferRecord', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var ListController = require('web.ListController');
    var Dialog = require('web.Dialog');

    ListController.include({
        _getActionMenuItems: function (state) {
            if (!this.hasActionMenus || !this.selectedRecords.length) {
                return null;
            }
            const props = this._super(...arguments);
            const otherActionItems = [];
            if (this.isExportEnable) {
                otherActionItems.push({
                    description: _t("Export"),
                    callback: () => this._onExportData()
                });
            }
            if (this.archiveEnabled) {
                otherActionItems.push({
                    description: _t("Archive"),
                    callback: () => {
                        Dialog.confirm(this, _t("Are you sure that you want to archive all the selected records?"), {
                            confirm_callback: () => this._toggleArchiveState(true),
                        });
                    }
                }, {
                    description: _t("Unarchive"),
                    callback: () => this._toggleArchiveState(false)
                });
            }
            if (this.activeActions.delete) {
                otherActionItems.push({
                    description: _t("Delete"),
                    callback: () => this._onDeleteSelectedRecords()
                });
            }
            if (this.modelName == 'res.partner') {
                otherActionItems.push({
                    description: _t("Transfer Record"),
                    callback: () => this._onTransferRecordData()
                });
            }
            return Object.assign(props, {
                items: Object.assign({}, this.toolbarActions, { other: otherActionItems }),
                context: state.getContext(),
                domain: state.getDomain(),
                isDomainSelected: this.isDomainSelected,
            });
        },
        _onTransferRecordData: function(ev){
            var self = this;
            this.do_action({
                name: '',
                type: 'ir.actions.act_window',
                res_model: 'transfer.record',
                target: 'new',
                views: [[false, 'form']],
                context: {'res_ids': self.getSelectedIds(), 'res_model': this.getSelectedRecords()[0].model}
            });
        },
    });

    core.action_registry.add('prism_instance_transfer.TransferRecord', ListController);
    return ListController;
});