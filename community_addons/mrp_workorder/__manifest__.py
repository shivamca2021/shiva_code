# -*- encoding: utf-8 -*-

{
    'name': 'MRP II',
    'version': '',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 51,
    'summary': """Work Orders, Planning, Stock Reports.""",
    'depends': ['quality', 'mrp', 'barcodes'],
    'description': """MRP Workorder
* Work order planning.  Check planning by Gantt views grouped by production order / work center
* Traceability report
* Cost Structure report (mrp_account)""",
    'data': [
        'security/ir.model.access.csv',
        'security/mrp_workorder_security.xml',
        'data/mrp_workorder_data.xml',
        'views/quality_views.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_workorder_views.xml',
        'views/mrp_workcenter_views.xml',
        'views/res_config_settings_view.xml',
        'wizard/additional_product_views.xml'
    ],
    'qweb': [
        'static/src/xml/mrp_workorder_barcode.xml',
    ],
    'demo': [
        'data/mrp_production_demo.xml',
        'data/mrp_workorder_demo.xml'
    ],
    'application': False,
}
