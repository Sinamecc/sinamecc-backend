from users.models import Module

_modules = [
    {
        'name': 'PPCN',
        'code': 'ppcn',
    },
    {
        'name': 'Mitigation Actions',
        'code': 'mitigation_action',
    },
    {
        'name': 'Adaptation Actions',
        'code': 'adaptation_action',
    },
    {
        'name': 'Report Data',
        'code': 'report_data',
    },
    {
        'name': 'MCCR',
        'code': 'mccr',
    },
]

for _module in _modules:
     Module.objects.get_or_create(**_module)
