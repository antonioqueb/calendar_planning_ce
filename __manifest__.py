{
    'name': 'Calendar Planning CE',
    'version': '1.0',
    'summary': 'Planificación de proyectos basada en el calendario para la edición Community.',
    'description': """
        Este módulo proporciona una vista de planificación temporal basada en la vista de calendario
        de Odoo Community Edition, simulando algunas funcionalidades de la vista Gantt.
    """,
    'author': 'Alphaqueb Consulting SAS',
    'website': 'http://www.alphaqueb.com',
    'category': 'Project Management',
    'depends': ['base', 'project'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/temporal_planning_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
