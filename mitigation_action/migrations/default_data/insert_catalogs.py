from mitigation_action.models import CategoryIPCC2006, SectorIPCC2006, SubCategoryIPCC2006, Sector
from mitigation_action.migrations.default_data import ipcc2006_catalogs

def insert_ipcc2006_catalogs():
    
    for sector in ipcc2006_catalogs.sector:
        sector_ipcc2006_list = sector.pop('sector_ipcc')
        sector_instance = Sector(**sector)
        sector_instance.save()
        
        for sector_ipcc2006 in sector_ipcc2006_list:
            category_list = sector_ipcc2006.pop('category')
            sector_ipcc2006_instance = SectorIPCC2006(**sector_ipcc2006, sector=sector_instance)
            sector_ipcc2006_instance.save()
            for category in category_list:
                sub_category_list = category.pop('sub_category')
                catetgory_ipcc_2006_instance = CategoryIPCC2006(**category, sector_ipcc_2006=sector_ipcc2006_instance)
                catetgory_ipcc_2006_instance.save()
                for sub_category in sub_category_list:
                    sub_category_ipcc_2006 = SubCategoryIPCC2006(**sub_category, category_ipcc_2006=catetgory_ipcc_2006_instance)
                    sub_category_ipcc_2006.save()



insert_ipcc2006_catalogs()
