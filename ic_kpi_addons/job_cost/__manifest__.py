# -*- coding: utf-8 -*-
{
    "name": "Job Cost",

    "summary": """
        Record Job Cost in Odoo""",

    "description": """
        Record Job Cost in Odoo
    """,

    "author": "Codeox",
    "website": "",
    "support": "",
    "license": "OPL-1",
    "category": "MRP",
    "version": "14.0.0.1",
    "depends": ["base","mrp","hr_attendance", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/job_cost_view.xml",
        "views/templates.xml",
        # "views/res_users_view.xml",
        "views/hr_employee.xml",
    ],
    'qweb': [
        "static/src/xml/job_cost_template.xml",
    ],
}