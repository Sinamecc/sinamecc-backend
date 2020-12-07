from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from ppcn.serializers import RequiredLevel, RecognitionTypeSerializer, RequiredLevelSerializer, SectorSerializer, SubSector, SubSectorSerializer

required_level = [
    {
        'level_type_es': 'Solicitud inicial',
        'level_type_en': 'Initial Request'
    },
    {
        'level_type_es': 'Seguimiento I',
        'level_type_en': 'Follow Up I'
    },

    {
        'level_type_es': 'Seguimiento II',
        'level_type_en': 'Follow Up II'
    },
    {
        'level_type_es': 'Renovación',
        'level_type_en': 'Renewal'
    }
]

recognition_type = [
    {
        'recognition_type_es': 'Carbono Inventario',
        'recognition_type_en': 'Carbon Inventary'
    },
    {
        'recognition_type_es': 'Carbono Reducción',
        'recognition_type_en': 'Carbon Reduction'
    },
    {
        'recognition_type_es': 'Carbono Reducción +',
        'recognition_type_en': 'Carbon Reduction +'
    },
    {
        'recognition_type_es': 'Carbono Neutralidad',
        'recognition_type_en': 'Carbon Neutrality'
    },
    {
        'recognition_type_es': 'Carbono Neutralidad +',
        'recognition_type_en': 'Carbon Neutrality +'
    }
]

organizational_sector = [
    {
        'name_es':'Agropecuario',
        'name_en': 'agricultural ',
        'sub_sector':[
            {
                'name_es': 'Agricultura',
                'name_en': 'Agriculture',
            },
            {
                'name_es': 'Ganadero y Pecuario',
                'name_en': 'Livestock',
            },
            {
                'name_es': 'Pesca',
                'name_en': 'Fishing',
            }
        ]
        
    },
    {
        'name_es':'USCUSyS',
        'name_en': 'USCUSyS',
        'sub_sector':[
            {
                'name_es': 'Uso de suelos',
                'name_en': 'Land Use',
            },
            {
                'name_es': 'Cambio de uso de suelo',
                'name_en': 'Land-use change',
            },
            {
                'name_es': 'Silvicultura',
                'name_en': 'Silviculture',
            },
        ]
    },
    {
        'name_es':'Transporte',
        'name_en': 'Transport',
        'sub_sector':[
            {
                'name_es': 'Transporte de carga pesada',
                'name_en': 'Heavy Load Transport',
            },
            {
                'name_es': 'Transporte y almacenamiento de productos',
                'name_en': 'Transportation and storage of products',
            },
            {
                'name_es': 'Transporte de pasajeros',
                'name_en': 'Passenger transport',
            },
        ]
    },
    {
        'name_es':'Comercio',
        'name_en': 'Commerce',
        'sub_sector':[
            {
                'name_es': 'Equipos agroforestales',
                'name_en': 'Agroforestry equipment',
            },
            {
                'name_es': 'Maquinaria y equipos',
                'name_en': 'Machinery and equipment',
            },
            {
                'name_es': 'Mobiliarios',
                'name_en': 'Furniture',
            },
            {
                'name_es': 'Vehículos',
                'name_en': 'Vehicles',
            },
            {
                'name_es': 'Comercio al por mayor y al por menor',
                'name_en': 'Wholesale and Retail',
            },
        ]
    },
    {
        'name_es':'Energía',
        'name_en': 'Energy',
        'sub_sector':[
            {
                'name_es': 'Suministro y distribución de electricidad, gas, vapor y aire acondicionado',
                'name_en': 'Supply and distribution of electricity, gas, steam and air conditioning',
            }
        ]
    },
    {
        'name_es':'Industria',
        'name_en': 'Industry',
        'sub_sector':[
            {
                'name_es': 'Industrias manufactureras',
                'name_en': 'Manufacturing industries',
            },
            {
                'name_es': 'Industria cementera',
                'name_en': 'Cement industry',
            },
            {
                'name_es': 'Industria de dispositivos médicos',
                'name_en': 'Medical device industry',
            },
            {
                'name_es': 'Industria farmacéutica',
                'name_en': 'Medical device industry',
            },
            {
                'name_es': 'Industria metalúrgica',
                'name_en': 'Metallurgical industry',
            },
            {
                'name_es': 'Industria alimentaria',
                'name_en': 'Food industry',
            },
            {
                'name_es': 'Industria química',
                'name_en': 'Chemical industry',
            },
            {
                'name_es': 'Construcción ',
                'name_en': 'Construction',
            },
            {
                'name_es': 'Otros procesos industriales ',
                'name_en': 'Other industrial processes',
            },
        ]
    },
    {
        'name_es':'Residuos',
        'name_en': 'Waste',
        'sub_sector':[
            {
                'name_es': 'Manejo y tratamiento de aguas residuales',
                'name_en': 'Wastewater management and treatment',
            },
            {
                'name_es': 'Manejo y disposición de residuos sólidos',
                'name_en': 'Solid waste management and disposal',
            },
            {
                'name_es': 'Coprocesamiento',
                'name_en': 'Co-processing',
            }
        ]
    },
    {
        'name_es':'Servicios',
        'name_en': 'Services',
        'sub_sector':[
            {
                'name_es': 'Suministro de servicios',
                'name_en': 'Provision of services',
            },
            {
                'name_es': 'Turismo, alojamiento y servicio de comidas',
                'name_en': 'Tourism, accommodation and food service',
            },
            {
                'name_es': 'Actividades financieras y de seguros',
                'name_en': 'Financial and insurance activities',
            },
            {
                'name_es': 'Actividades profesionales, científicas y técnicas',
                'name_en': 'Professional, scientific and technical activities',
            },
            {
                'name_es': 'Administración pública y defensa',
                'name_en': 'Public administration and defense',
            },
            {
                'name_es': 'Educación',
                'name_en': 'Education',
            },
            {
                'name_es': 'Actividades de atención de la salud humana y de asistencia social',
                'name_en': 'Human health care and social assistance activities',
            }
            
        ]
    },
    {
        'name_es':'Otros',
        'name_en': 'Others',
        'sub_sector':[
            {
                'name_es': 'Otras actividades',
                'name_en': 'Other activities',
            }
        ]
    }

]


def reset_catalogs_data(apps, schema_editor):
    RequiredLevel = apps.get_model("ppcn", "RequiredLevel")
    RecognitionType = apps.get_model("ppcn", "RecognitionType")
    Sector = apps.get_model("ppcn", "Sector")
    GeographicLevel = apps.get_model("ppcn", "GeographicLevel") 
    
    RequiredLevel.objects.all().delete()
    RecognitionType.objects.all().delete()
    sector_list = Sector.objects.filter(geographicLevel__level_es='Organizacional').all()
    geograohic_level = GeographicLevel.objects.filter(level_es='Organizacional').last()
    for sector in sector_list:
        sector.sector.all().delete()
        sector.delete()

    serialized_required = RequiredLevelSerializer(data=required_level, many=True)
    serialized_required.is_valid()
    serialized_required.save()
    serialized_recognition_type = RecognitionTypeSerializer(data=recognition_type, many=True)
    serialized_recognition_type.is_valid()
    serialized_recognition_type.save()

    sub_sector_list_serialized = []
    for sector in organizational_sector:
        sub_sector_list = sector.pop('sub_sector')
        sector['geographicLevel'] = geograohic_level.id
        serialized_sector = SectorSerializer(data=sector)
        
        if serialized_sector.is_valid():
            saved_sector = serialized_sector.save()
            
            for sub_sector in sub_sector_list:
                sub_sector_list_serialized.append({**sub_sector, 'sector':saved_sector.id})
        else:
            print(serialized_sector.errors)
            
    sub_sector_serialized_list = SubSectorSerializer(data=sub_sector_list_serialized, many=True)
    if sub_sector_serialized_list.is_valid():
        sub_sector_serialized_list.save()
    else:
        print(sub_sector_serialized_list.errors)





    

class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0027_auto_20200805_1755'),
    ]
    operations = [
       
        migrations.RunPython(reset_catalogs_data, reverse_code=migrations.RunPython.noop)
    ]

    


    
