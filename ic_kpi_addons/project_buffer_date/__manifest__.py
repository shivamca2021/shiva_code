{
    'name': 'Project Buffer Day Management',
    'category': 'Project',
    'summary': 'Project Buffer Day Management.',
    'version': '1.0',
    'description': """Project Buffer Day Management""",
    'depends': [
        'project',
        'cki_project_custom',
        'dhx_gantt'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_stage.xml',
        'views/assest.xml',
        
    ],
    'qweb': [
       
        "static/src/xml/web_calendar.xml",
    ],
    'installable': True,
    'auto_install': False,
}
