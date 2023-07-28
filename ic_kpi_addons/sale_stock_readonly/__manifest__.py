# -*- coding: utf-8 -*-
{
    "name": "Sales Stock Readonly",

    "summary": """
        Sales Stock Readonly""",

    "description": """
        Sales Stock Readonly
    """,

    "author": "Codeox",
    "website": "",
    "support": "",
    "license": "OPL-1",
    "category": "Sales",
    "version": "14.0.0.1",
    "depends": ["base","sale","stock", "purchase"],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/sale_views.xml",
        "views/stock_views.xml",
        "views/purchase_views.xml",
    ],
}