{
    'name': 'Project Management',
    'category': 'Project',
    'summary': 'Project Management.',
    'version': '1.0',
    'description': """Project Management""",
    'depends': [
        'project','hr_timesheet','web_icon_change_project'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_stage.xml',
        'wizard/capacity_confirm.xml',
        'views/assest.xml',
    ],
    'installable': True,
    'auto_install': False,
}
