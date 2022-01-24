from adaptation_action.models import Classifier


_report_organization_type = [ 
    {
        'entity_type': 'Entidad pública',
        'code': '1'
    },
    {
        'entity_type': 'Entidad privada',
        'code': '2'
    },
    {
        'entity_type': 'Municipalidad',
        'code': '3'
    },
    {
        'entity_type': 'ONG',
        'code': '4'
    }
]

_adaptation_action_type = [ 
    {
        'name': 'Tipo A - Instrumentos de políticas y planes',
        'code': '1'
    },
    {
        'name': 'Tipo B - Proyecto y programas',
        'code': '2'
    },
    {
        'name': 'Tipo C - Actividad',
        'code': '3'
    }
]

_type_climate_threat = [ 
    {
        'name': 'Deslizamiento',
        'code': '1'
    },
    {
        'name': 'Inundación',
        'code': '2'
    },
    {
        'name': 'Avenida torrencial',
        'code': '3'
    },
    {
        'name': 'Ola de calor',
        'code': '4'
    },
    {
        'name': 'Sequía',
        'code': '5',
    },
    {
        'name': 'Altos niveles de precipitación',
        'code': '6'
    },
    {
        'name': 'Bajas temperaturas (heladas)',
        'code': '7'
    },
    {
        'name': 'Huracanes',
        'code': '8'
    },
    {
        'name': 'Incremento del nivel de agua',
        'code': '9'
    },
    {
        'name': 'Vendavales',
        'code': '10'
    },
    {
        'name': 'Vientos de alta velocidad',
        'code': '11'
    },
    {
        'name': 'Tormentas eléctricas',
        'code': '12'
    },
    {
        'name': 'Incendios forestales',
        'code': '13'
    },
    {
        'name': 'Fénomeno del niño',
        'code': '14'
    },
    {
        'name': 'Fenómeno de la niña',
        'code': '15'
    },
    {
        'name': 'Cambios en los patrones estacionales',
        'code': '16'
    },
    {
        'name': 'Otros',
        'code': '17'
    }
]

_ODS_data = [
    {
        'code': '1',
        'name': 'Fin de la pobreza.',
    },
    {
        'code': '2',
        'name': 'Hambre cero.',
    },
    {
        'code': '3',
        'name': 'Salud y bienestar.',
    },
    {
        'code': '4',
        'name': 'Educación de calidad.',
    },
    {
        'code': '5',
        'name': 'Igualdad de género.',
    },
    {
        'code': '6',
        'name': 'Agua limpia y saneamiento.',
    },
    {
        'code': '7',
        'name': 'Energía asequible y no contaminante.',
    },
    {
        'code': '8',
        'name': 'Trabajo decente y crecimiento económico.',
    },
    {
        'code': '9',
        'name': 'Industria, innovación e infraestructura.',
    },
    {
        'code': '10',
        'name': 'Reducción de las desigualdades.',
    },
    {
        'code': '11',
        'name': 'Ciudades y comunidades sostenibles.',
    },
    {
        'code': '12',
        'name': 'Producción y consumo responsable.',
    },
    {
        'code': '13',
        'name': 'Acción por el clima.',
    },
    {
        'code': '14',
        'name': 'Vida submarina.',
    },
    {
        'code': '15',
        'name': 'Vida de ecosistemas terrestres.',
    },
    {
        'code': '16',
        'name': 'Paz, justicia e instituciones sólidas.',
    },
    {
        'code': '17',
        'name': 'Alianzas para lograr los objetivos.',
    }
]

_finance_source = [
    {
        'name': 'Presupuesto público nacional.',
        'code': '1'
    },
    {
        'name': 'Presupuesto privado nacional.',
        'code': '2'
    },
    {
        'name': 'Cooperación internacional.',
        'code': '3'
    },
    {
        'name': 'Por definir.',
        'code': '4'
    }
]

_instrument_detail = [
    {
        'name': 'Fondos.',
        'code': '1'
    },
    {
        'name': 'Préstamos tradicionales.',
        'code': '2'
    },
    {
        'name': 'Préstamos concensionales.',
        'code': '3'
    },
    {
        'name': 'Subsidios.',
        'code': '4'
    },
    {
        'name': 'Garatnías.',
        'code': '5'
    },
    {
        'name': 'Fideicomisos.',
        'code': '6'
    },
    {
        'name': 'Canjes de deuda.',
        'code': '7'
    },
    {
        'name': 'Otros.',
        'code': '8'
    }
]

_source_type = [ 
    {
        'name': 'Censos',
        'code': '1'
    },
    {
        'name': 'Encuesta por muestreo',
        'code': '2'
    },
    {
        'name': 'Combinación de censos y muestreos',
        'code': '3'
    },
    {
        'name': 'Sondeos de opinión',
        'code': '4'
    },
    {
        'name': 'Registro administrativo',
        'code': '5'
    },
    {
        'name': 'Sistema de Monitorio',
        'code': '6'
    },
    {
        'name': 'Estimación directa',
        'code': '7'
    },
    {
        'name': 'Actas',
        'code': '8'
    },
    {
        'name': 'Lista de asistencia',
        'code': '9'
    },
    {
        'name': 'Mapas',
        'code': '10'
    },
    {
        'name': 'Otro',
        'code': '11'
    }
]

_thematic_data = [
    {
        'name': 'Gestión',
        'code': '1'
    },
    {
        'name': 'Resultado',
        'code': '2'
    },
    {
        'name': 'Otro',
        'code': '3'
    }
]

_classifier_sinamecc = [ 
    {
        'name': 'Acción Climática',
        'code': '1'
    },
    {
        'name': 'Modelación',
        'code': '2'
    },
    {
        'name': 'INGEI',
        'code': '3'
    },
    {
        'name': 'Reportes',
        'code': '4'
    },
    {
        'name': 'Finanzas Climaticas',
        'code': '5'
    },
    {
        'name': 'Impactos',
        'code': '6'
    },
    {
        'name': 'Otro',
        'code': '7'
    }
]

_general_impact = [
    {
        'name': 'Aumento de resiliencia',
        'code': '1'
    },
    {
        'name': 'Disminución de vulnerabilidad',
        'code': '2' 
    },
    {
        'name': 'Mitigación de riego',
        'code': '3'
    },
    {
        'name': 'Creción de capacidades',
        'code': '4'
    },
    {
        'name': 'MConocimiento sobre amenazas',
        'code': '5'
    },
    {
        'name': 'Planeación basada en el cambio climático',
        'code': '6'
    },
]

_temporality_impact = [
    {
        'name': 'Inmediato',
        'code': '1'
    },
    {
        'name': 'Corto plazo (hasta 1 año)',
        'code': '2'
    },
    {
        'name': 'Mediano plazo (entre 1 - 5 años)',
        'code': '3'
    },
    {
        'name': 'Largo plazo (más de 5 años)',
        'code': '4'
    }
]



