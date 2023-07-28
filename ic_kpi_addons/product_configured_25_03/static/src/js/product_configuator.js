odoo.define('product_configured.ProductConfigured', function (require) {
"use strict";

var core = require('web.core');
var _t = core._t;
var ProductConfiguratorFormController = require('sale_product_configurator.ProductConfiguratorFormController');
var ProductConfiguratorFormRenderer = require('sale_product_configurator.ProductConfiguratorFormRenderer');
var ProductConfiguratorWidget = require('sale.product_configurator');

ProductConfiguratorFormRenderer.include({

    renderConfigurator: function (configuratorHtml) {
        this._super.apply(this, arguments);
        var self = this;

        var partProducts = [];
        _.each( this.state.data.part_ids.data, function(part) {
            partProducts.push(part.res_id);
        });
        if (partProducts.length > 0)
            self.partProducts = partProducts;
        else
            self.partProducts = [];

        var subAssemblyProducts = [];
        _.each( this.state.data.sub_assembly_ids.data, function(subassembly) {
            subAssemblyProducts.push(subassembly.res_id);
        });
        if (subAssemblyProducts.length > 0)
            self.subAssemblyProducts = subAssemblyProducts;
        else
            self.subAssemblyProducts = [];

        var materialProducts = [];
        console.log(">>>>>>>>>>>this.state.data >>>>>>>>>>",this.state.data);
        if (this.state.data.material_ids) {
            _.each( this.state.data.material_ids.data, function(material) {
                materialProducts.push(material.res_id);
            });
            if (materialProducts.length > 0)
                self.materialProducts = materialProducts;
            else
                self.materialProducts = [];
        }
        else
            self.materialProducts = [];

        var speciesProducts = [];
        if (this.state.data.species_ids) {
            _.each( this.state.data.species_ids.data, function(species) {
                speciesProducts.push(species.res_id);
            });
            if (speciesProducts.length > 0)
                self.speciesProducts = speciesProducts;
            else
                self.speciesProducts = [];
        }
        else
            self.speciesProducts = [];

        var internalProducts = [];
        if (this.state.data.internal_material_ids) {
            _.each( this.state.data.internal_material_ids.data, function(internal) {
                internalProducts.push(internal.res_id);
            });
            if (internalProducts.length > 0)
                self.internalProducts = internalProducts;
            else
                self.internalProducts = [];
        }
        else
            self.internalProducts = [];

        var externalProducts = [];
        if (this.state.data.external_material_ids) {
            _.each( this.state.data.external_material_ids.data, function(external) {
                externalProducts.push(external.res_id);
            });
            if (externalProducts.length > 0)
                self.externalProducts = externalProducts;
            else
                self.externalProducts = [];
        }
        else
            self.externalProducts = [];

        this.$el.find('input[type="checkbox"]').filter('[part-data-id]').click(function (event) {
            var part = event.currentTarget;
            if ($(part)[0].checked) {
                if ($.inArray($(part).attr('part-data-id'), self.partProducts) == -1) {
                    self.partProducts.push($(part).attr('part-data-id'));
                }
            } else {
                var res = self.partProducts.filter(function (i) {
                    return i != $(part).attr('part-data-id');
                });
                self.partProducts = res;
            }
            self.partProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
        this.$el.find('input[type="checkbox"]').filter('[subassembly-data-id]').click(function (event) {
            var subassembly = event.currentTarget;
            if ($(subassembly)[0].checked) {
                if ($.inArray($(subassembly).attr('subassembly-data-id'), self.subAssemblyProducts) == -1) {
                    self.subAssemblyProducts.push($(subassembly).attr('subassembly-data-id'));
                }
            } else {
                var res = self.subAssemblyProducts.filter(function (i) {
                    return i != $(subassembly).attr('subassembly-data-id');
                });
                self.subAssemblyProducts = res;
            }
            self.subAssemblyProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
        this.$el.find('input[type="checkbox"]').filter('[material-product-data-id]').click(function (event) {
            var material = event.currentTarget;
            if ($(material)[0].checked) {
                if ($.inArray($(material).attr('material-product-data-id'), self.materialProducts) == -1) {
                    self.materialProducts.push($(material).attr('material-product-data-id'));
                }
            } else {
                var res = self.materialProducts.filter(function (i) {
                    return i != $(material).attr('material-product-data-id');
                });
                self.materialProducts = res;
            }
            self.materialProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
        this.$el.find('input[type="checkbox"]').filter('[species-product-data-id]').click(function (event) {
            var species = event.currentTarget;
            if ($(species)[0].checked) {
                if ($.inArray($(species).attr('species-product-data-id'), self.speciesProducts) == -1) {
                    self.speciesProducts.push($(species).attr('species-product-data-id'));
                }
            } else {
                var res = self.speciesProducts.filter(function (i) {
                    return i != $(species).attr('species-product-data-id');
                });
                self.speciesProducts = res;
            }
            self.speciesProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
        this.$el.find('input[type="checkbox"]').filter('[internal-product-data-id]').click(function (event) {
            var internal = event.currentTarget;
            if ($(internal)[0].checked) {
                if ($.inArray($(internal).attr('internal-product-data-id'), self.internalProducts) == -1) {
                    self.internalProducts.push($(internal).attr('internal-product-data-id'));
                }
            } else {
                var res = self.internalProducts.filter(function (i) {
                    return i != $(species).attr('internal-product-data-id');
                });
                self.internalProducts = res;
            }
            self.internalProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
        this.$el.find('input[type="checkbox"]').filter('[external-product-data-id]').click(function (event) {
            var external = event.currentTarget;
            if ($(external)[0].checked) {
                if ($.inArray($(external).attr('external-product-data-id'), self.externalProducts) == -1) {
                    self.externalProducts.push($(external).attr('external-product-data-id'));
                }
            } else {
                var res = self.externalProducts.filter(function (i) {
                    return i != $(external).attr('external-product-data-id');
                });
                self.externalProducts = res;
            }
            self.externalProducts.filter((x, i, a) => a.indexOf(x) == i);
        });
    },
});
ProductConfiguratorWidget.include({

    _getMainProductChanges: function (mainProduct) {
        var partLineIds = mainProduct.parts;
        var result = this._super.apply(this, arguments);
        var noPartCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(partLineIds, function (noPartId) {
            return {id: parseInt(noPartId)};
        });
        noPartCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['part_ids'] = {
            operation: 'MULTI',
            commands: noPartCommands
        };

        var subassemblyLineIds = mainProduct.subassembly;
        var noSubassemblyCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(subassemblyLineIds, function (noSubassemblyId) {
            return {id: parseInt(noSubassemblyId)};
        });
        noSubassemblyCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['sub_assembly_ids'] = {
            operation: 'MULTI',
            commands: noSubassemblyCommands
        };

        var materialLineIds = mainProduct.material;
        var noMaterialCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(materialLineIds, function (noMaterialId) {
            return {id: parseInt(noMaterialId)};
        });
        noMaterialCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['material_ids'] = {
            operation: 'MULTI',
            commands: noMaterialCommands
        };
        var internalLineIds = mainProduct.internal;
        var noInternalCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(internalLineIds, function (noInternalId) {
            return {id: parseInt(noInternalId)};
        });
        noInternalCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['internal_material_ids'] = {
            operation: 'MULTI',
            commands: noInternalCommands
        };

        var externalLineIds = mainProduct.external;
        var noExternalCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(externalLineIds, function (noeExternalId) {
            return {id: parseInt(noeExternalId)};
        });
        noExternalCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['external_material_ids'] = {
            operation: 'MULTI',
            commands: noExternalCommands
        };

        var speciesLineIds = mainProduct.species;
        var noSpeciesCommands = [{operation: 'DELETE_ALL'}];
        var resIds = _.map(speciesLineIds, function (noSpeciesId) {
            return {id: parseInt(noSpeciesId)};
        });
        noSpeciesCommands.push({
            operation: 'ADD_M2M',
            ids: resIds
        });
        result['species_ids'] = {
            operation: 'MULTI',
            commands: noSpeciesCommands
        };
        return result;
    },

    _onEditProductConfiguration: function () {
        if (!this.recordData.is_configurable_product) {
            // if line should be edited by another configurator
            // or simply inline.
            this._super.apply(this, arguments);
            return;
        }
        // If line has been set up through the product_configurator:
        this._openProductConfigurator({
                configuratorMode: 'edit',
                default_product_template_id: this.recordData.product_template_id.data.id,
                default_pricelist_id: this._getPricelistId(),
                default_product_template_attribute_value_ids: this._convertFromMany2Many(
                    this.recordData.product_template_attribute_value_ids
                ),
                default_product_no_variant_attribute_value_ids: this._convertFromMany2Many(
                    this.recordData.product_no_variant_attribute_value_ids
                ),
                default_product_custom_attribute_value_ids: this._convertFromOne2Many(
                    this.recordData.product_custom_attribute_value_ids
                ),
                default_quantity: this.recordData.product_uom_qty,
                default_part_ids: this._convertFromMany2Many(
                    this.recordData.part_ids
                ),
                default_sub_assembly_ids: this._convertFromMany2Many(
                    this.recordData.sub_assembly_ids
                ),
                default_material_ids: this._convertFromMany2Many(
                    this.recordData.material_ids
                ),
                default_internal_material_ids: this._convertFromMany2Many(
                    this.recordData.internal_material_ids
                ),
                default_external_material_ids: this._convertFromMany2Many(
                    this.recordData.external_material_ids
                ),
                default_species_ids: this._convertFromMany2Many(
                    this.recordData.species_ids
                )
            },
            this.dataPointID
        );

    },
});
ProductConfiguratorFormController.include({

    _configureProduct: function (productTemplateId) {
        var self = this;
        var initialProduct = this.initialState.data.product_template_id;
        var changed = initialProduct && initialProduct.data.id !== productTemplateId;
        var data = this.renderer.state.data;
        return this._rpc({
            route: '/sale_product_configurator/configure',
            params: {
                product_template_id: productTemplateId,
                pricelist_id: this.renderer.pricelistId,
                add_qty: data.quantity,
                product_template_attribute_value_ids: changed ? [] : this._getAttributeValueIds(
                    data.product_template_attribute_value_ids
                ),
                product_no_variant_attribute_value_ids: changed ? [] : this._getAttributeValueIds(
                    data.product_no_variant_attribute_value_ids
                ),
                part_ids: changed ? [] : this._getAttributeValueIds(
                    data.part_ids
                ),
                sub_assembly_ids: changed ? [] : this._getAttributeValueIds(
                    data.sub_assembly_ids
                ),
                material_ids: changed ? [] : this._getAttributeValueIds(
                    data.material_ids
                ),
                internal_material_ids: changed ? [] : this._getAttributeValueIds(
                    data.internal_material_ids
                ),
                external_material_ids: changed ? [] : this._getAttributeValueIds(
                    data.external_material_ids
                ),
            }
        }).then(function (configurator) {
            self.renderer.configuratorHtml = configurator;
        });
    },

    _onAddRootProductOnly: function () {
        this.rootProduct['parts'] = this.renderer.partProducts;
        this.rootProduct['subassembly'] = this.renderer.subAssemblyProducts;
        this.rootProduct['material'] = this.renderer.materialProducts;
        this.rootProduct['internal'] = this.renderer.internalProducts;
        this.rootProduct['external'] = this.renderer.externalProducts;
        this.rootProduct['species'] = this.renderer.speciesProducts;
        this._addProducts([this.rootProduct]);
    },

    _addProducts: function(products) {
        products[0]['parts'] = this.renderer.partProducts;
        products[0]['subassembly'] = this.renderer.subAssemblyProducts;
        products[0]['material'] = this.renderer.materialProducts;
        products[0]['internal'] = this.renderer.internalProducts;
        products[0]['external'] = this.renderer.externalProducts;
        products[0]['species'] = this.renderer.speciesProducts;
        this._super.apply(this, arguments);
    },
});
});
