odoo.define('product_configured.searchUtils', function (require) {
    "use strict";

    const { _lt, _t } = require('web.core');
    const { FIELD_OPERATORS } = require('web.searchUtils');

    var custom_operators = FIELD_OPERATORS;

    custom_operators.char.push(
        { symbol: "=ilike", description: _lt("Start With") },
        { symbol: "like", description: _lt("End With") },
    );
    });