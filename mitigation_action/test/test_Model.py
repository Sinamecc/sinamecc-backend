from typing import ClassVar
from django.db.models import fields
from django.test import TestCase, Client
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService

from datetime import datetime
from mitigation_action.models import *
from mitigation_action.serializers import *

# initialize the APIClient app
client = Client()


class MitigationActionModelTest(TestCase):

    def setUp(self):

        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        client.force_login(self.user)
        
        self.mitigation_service = MitigationActionService()
        self.contact = Contact.objects.create(institution="institution test", full_name="full_name test", job_title="job_test", email="email@email.com", phone="88888888",
        user=self.user)
        self.status = Status.objects.create(status="status_test", code="0")        
        self.finance_status = FinanceStatus.objects.create(name="finance_status", code="00")
        self.finance_source = FinanceSourceType.objects.create(name="finance_source", code="01")
        self.geographic_scale = GeographicScale.objects.create(name="geographic_scale", code="02")
        self.initiative_type = InitiativeType.objects.create(name="initiative_type", code="03")

        self.finance = Finance.objects.create(status=self.finance_status, administration="admin_test", source=self.finance_source, source_description="source_description",
            reference_year=2000, budget=1, mideplan_registered=True, mideplan_project="mideplan_project_test", executed_entity="exec_entity_test")
        self.geographic_location = GeographicLocation.objects.create(geogrpahic_scale=self.geographic_scale, location="location_test")
        self.initiative = Initiative.objects.create(name="name_initiative", objective="objetive_test", description="description_test", initiative_type=self.initiative_type)
        self.initiative_goal = InitiativeGoal.objects.create(goal="goal_test", initiative=self.initiative)
        self.mitigation_action_status = MitigationActionStatus.objects.create(status=self.status, start_date=datetime.datetime(2007, 1, 1), end_date=datetime.datetime(2008, 1, 1), other_end_date=datetime.datetime(2009, 1, 1),
            institution="institution_test_mitigation", other_institution="other_institution_test")
        self.ghg_information = GHGInformation.objects.create(impact_emission="impact_emission_test", graphic_description="graphic_description_test")

        ##
        self.impact_category = ImpactCategory.objects.create(code= "00", name="impact_category_test")
        self.carbon_deposit = CarbonDeposit.objects.create(code= "00", name="carbon_deposit_test")
        self.standard = Standard.objects.create(code= "00", name="standard_test")
        self.sustainable_dev_goals = SustainableDevelopmentGoals.objects.create(code= "00", description="sustainable_dev_goals_test_description")
        self.ghg_impact_sector = GHGImpactSector.objects.create(code= "00", name="ghg_impact_sector_test")
        ##Preguntar a Izcar si en descripcipones no sale nada dentro de los parentesis
        self.action_area = ActionAreas.objects.create(code= "00", name="action_areas_test")
        self.action_goal = ActionGoals.objects.create(code = "00", area = self.action_area)
        self.descarbonization_axis = DescarbonizationAxis.objects.create(code = "00", description = "descarbonization_axis_test")
        self.transformational_vision = TransformationalVisions.objects.create(code = "00", axis = self.descarbonization_axis)
        self.topic = Topics.objects.create(code= "00", name="topics_test")
        self.sub_topic = SubTopics.objects.create(code= "00", name="subtopics_test", topic = self.topic)
        self.activity = Activity.objects.create(code = "00", sub_topic = self.sub_topic)
        self.thematic_categorization_type = ThematicCategorizationType.objects.create(code= "00", name="thematic_categorization_type_test")
        self.information_source_type = InformationSourceType.objects.create(name="information_soruce_type_test")
        self.classifier = Classifier.objects.create(code= "00", name="classifier_test")
        self.monitoring_reporting_indicator = MonitoringReportingIndicator.objects.create(progress_in_monitoring = True)
        self.monitoring_information = MonitoringInformation.objects.create(code = "00")
        self.impact_documentation = ImpactDocumentation.objects.create(estimate_reduction_co2 = "estimate_reduction_co2_test", period_potencial_reduction = "period_potencial_reduction_test",
            carbon_deposit = self.carbon_deposit, base_line_definition = "base_line_definition_test", calculation_methodology = "calculation_methodology_test",
            estimate_calculation_documentation = "estimate_calculation_documentation_test", mitigation_action_in_inventory = True, standard = self.standard, other_standar = "other_standar_test",
            carbon_international_commerce = True, methodologies_to_use = "methologies_to_use_test")
        self.categorization = Categorization.objects.create(is_part_to_another_mitigation_action = True, relation_description = "relation_description_test")
        self.information_source = InformationSource.objects.create(responsible_institution = "responsible_institution_test", type = self.information_source_type, other_type = "other_type_test",
        statistical_operation = "statistical_operation_test")
        self.indicator = Indicator.objects.create(name = "indicator_test", description = "description_test", unit = "unit_test", methodological_detail = "methodological_detail_test",
            reporting_periodicity = "reporting_periodicity_test", geographic_coverage = "geographic_coverage_test", disaggregation = "disaggregation_test", type_of_data = self.thematic_categorization_type,
            other_type_of_data = "other_type_of_data_test", contact = self.contact, monitoring_information = self.monitoring_information)
        self.indicator_classifier = IndicatorClassifier.objects.create(indicator = self.indicator, classifier = self.classifier, description = "description_test")
        self.monitoring_indicator = MonitoringIndicator.objects.create(initial_date_report_period =datetime.datetime(2007, 1, 1), final_date_report_period=datetime.datetime(2007, 1, 1), updated_data="updated_data_test",
            progress_report = "progress_report_test", indicator = self.indicator, monitoring_reporting_indicator=self.monitoring_reporting_indicator)
        self.qaq_reduction_estimate_question = QAQCReductionEstimateQuestion.objects.create(code = "00", question = "question_test", check = True, detail = "detail_test",
            impact_documentation = self.impact_documentation)
        self.mitigation_action = MitigationAction.objects.create(contact=self.contact, initiative=self.initiative, status_information=self.mitigation_action_status, 
            geographic_location = self.geographic_location, finance = self.finance, ghg_information = self.ghg_information, impact_documentation=self.impact_documentation, monitoring_information = self.monitoring_information,
            monitoring_reporting_indicator = self.monitoring_reporting_indicator, user = self.user)


    def mitigation_action_test(self):

        field_contact = self.mitigation_action.contact
        field_initiative = self.mitigation_action.initiative
        field_status_information = self.mitigation_action.status_information
        field_geographic_location = self.mitigation_action.geographic_location
        field_finance = self.mitigation_action.finance
        field_ghg_information = self.mitigation_action.ghg_information
        field_impact_documentation = self.mitigation_action.impact_documentation
        field_monitoring_information = self.mitigation_action.monitoring_information
        field_monitoring_reporting_indicator = self.mitigation_action.monitoring_reporting_indicator
        field_user = self.mitigation_action.user

        self.assertEquals(field_contact, self.contact)
        self.assertEquals(field_initiative, self.initiative)
        self.assertEquals(field_status_information, self.mitigation_action_status)
        self.assertEquals(field_geographic_location, self.geographic_location)
        self.assertEquals(field_finance, self.finance)
        self.assertEquals(field_ghg_information, self.ghg_information)
        self.assertEquals(field_impact_documentation, self.impact_documentation)
        self.assertEquals(field_monitoring_information, self.monitoring_information)
        self.assertEquals(field_monitoring_reporting_indicator, self.monitoring_reporting_indicator)
        self.assertEquals(field_user, self.user)


    def test_qaq_reduction_estimate_question(self):
        field_code = self.qaq_reduction_estimate_question.code
        field_question = self.qaq_reduction_estimate_question.question
        field_check = self.qaq_reduction_estimate_question.check
        field_detail = self.qaq_reduction_estimate_question.detail
        field_impact_documentation = self.qaq_reduction_estimate_question.impact_documentation

        self.assertEquals(field_code, "00")
        self.assertEquals(field_question, "question_test")
        self.assertEquals(field_check, True)
        self.assertEquals(field_detail, "detail_test")
        self.assertEquals(field_impact_documentation, self.impact_documentation)
    
    def test_monitoring_indicator(self):
        field_initial_date_report_period = self.monitoring_indicator.initial_date_report_period
        field_final_date_report_period = self.monitoring_indicator.final_date_report_period
        field_updated_data = self.monitoring_indicator.updated_data
        field_progress_report = self.monitoring_indicator.progress_report
        field_indicator = self.monitoring_indicator.indicator
        field_monitoring_reporting_indicator = self.monitoring_indicator.monitoring_reporting_indicator

        self.assertEquals(field_initial_date_report_period, datetime.datetime(2007, 1, 1))
        self.assertEquals(field_final_date_report_period, datetime.datetime(2007, 1, 1))
        self.assertEquals(field_updated_data, "updated_data_test")
        self.assertEquals(field_progress_report, "progress_report_test")
        self.assertEquals(field_indicator, self.indicator)
        self.assertEquals(field_monitoring_reporting_indicator, self.monitoring_reporting_indicator)

    def test_indicator_classifier(self):
        field_indicator = self.indicator_classifier.indicator
        field_classifier = self.indicator_classifier.classifier
        field_description = self.indicator_classifier.description

        self.assertEquals(field_indicator, self.indicator)
        self.assertEquals(field_classifier, self.classifier)
        self.assertEquals(field_description, "description_test")

    def test_indicator(self):
        field_name = self.indicator.name
        field_description = self.indicator.description
        field_unit = self.indicator.unit
        field_methodological_detail = self.indicator.methodological_detail
        field_reporting_periodicity = self.indicator.reporting_periodicity
        field_geographic_coverage = self.indicator.geographic_coverage
        field_disaggregation = self.indicator.disaggregation
        field_type_of_data = self.indicator.type_of_data
        field_other_type_of_data = self.indicator.other_type_of_data
        field_contact = self.indicator.contact
        field_monitoring_information = self.indicator.monitoring_information

        self.assertEquals(field_monitoring_information, self.monitoring_information)
        self.assertEquals(field_contact, self.contact)
        self.assertEquals(field_other_type_of_data, "other_type_of_data_test")
        self.assertEquals(field_type_of_data, self.thematic_categorization_type)
        self.assertEquals(field_disaggregation, "disaggregation_test")
        self.assertEquals(field_geographic_coverage, "geographic_coverage_test")
        self.assertEquals(field_reporting_periodicity, "reporting_periodicity_test")
        self.assertEquals(field_methodological_detail, "methodological_detail_test")
        self.assertEquals(field_unit, "unit_test")
        self.assertEquals(field_description, "description_test")
        self.assertEquals(field_name, "indicator_test")
    
    def test_information_source(self):
        field_responsible_institution = self.information_source.responsible_institution
        field_type = self.information_source.type
        field_other_type = self.information_source.other_type
        field_statistical_operation = self.information_source.statistical_operation

        self.assertEquals(field_statistical_operation, "statistical_operation_test")
        self.assertEquals(field_other_type, "other_type_test")
        self.assertEquals(field_type, self.information_source_type)
        self.assertEquals(field_responsible_institution, "responsible_institution_test")

    
    def test_categorization(self):
        field_is_part_to_another_mitigation_action = self.categorization.is_part_to_another_mitigation_action
        field_relation_description = self.categorization.relation_description

        self.assertEquals(field_is_part_to_another_mitigation_action, True)
        self.assertEquals(field_relation_description, "relation_description_test")

    def test_impact_documentation(self):
        field_estimate_reduction_co2 = self.impact_documentation.estimate_reduction_co2
        field_period_potencial_reduction = self.impact_documentation.period_potencial_reduction
        field_carbon_deposit = self.impact_documentation.carbon_deposit
        field_base_line_definition = self.impact_documentation.base_line_definition
        field_calculation_methodology = self.impact_documentation.calculation_methodology
        field_estimate_calculation_documentation = self.impact_documentation.estimate_calculation_documentation
        field_mitigation_action_in_inventory = self.impact_documentation.mitigation_action_in_inventory
        field_standard = self.impact_documentation.standard
        field_other_standar = self.impact_documentation.other_standar
        field_carbon_international_commerce = self.impact_documentation.carbon_international_commerce
        field_methodologies_to_use = self.impact_documentation.methodologies_to_use

        self.assertEquals(field_methodologies_to_use, "methologies_to_use_test")
        self.assertEquals(field_carbon_international_commerce, True)
        self.assertEquals(field_other_standar, "other_standar_test")
        self.assertEquals(field_standard, self.standard)
        self.assertEquals(field_mitigation_action_in_inventory, True)
        self.assertEquals(field_estimate_calculation_documentation, "estimate_calculation_documentation_test")
        self.assertEquals(field_calculation_methodology, "calculation_methodology_test")
        self.assertEquals(field_base_line_definition, "base_line_definition_test")
        self.assertEquals(field_carbon_deposit, self.carbon_deposit)
        self.assertEquals(field_estimate_reduction_co2, "estimate_reduction_co2_test")
        self.assertEquals(field_period_potencial_reduction, "period_potencial_reduction_test")
    
    def test_monitoring_information(self):
        field_code = self.monitoring_information.code

        self.assertEquals(field_code, "00")

    def test_monitoring_reporting_indicator(self):
        field_progress = self.monitoring_reporting_indicator.progress_in_monitoring

        self.assertEquals(field_progress, True)

    def test_classifier(self):
        field_code = self.classifier.code
        field_name = self.classifier.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "classifier_test")
    
    def test_information_source_type(self):
        field_name = self.information_source_type.name

        self.assertEquals(field_name, "information_soruce_type_test")
    
    def test_thematic_categorization_type(self):
        field_code = self.thematic_categorization_type.code
        field_name = self.thematic_categorization_type.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "thematic_categorization_type_test")
    
    def test_activity(self):
        field_code = self.activity.code
        field_sub_topic = self.activity.sub_topic

        self.assertEquals(field_code, "00")
        self.assertEquals(field_sub_topic, self.sub_topic)
    
    def test_sub_topic(self):
        field_code = self.sub_topic.code
        field_name = self.sub_topic.name
        field_topic = self.sub_topic.topic

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "subtopics_test")
        self.assertEquals(field_topic, self.topic)

    def test_topic(self):
        field_code = self.topic.code
        field_name = self.topic.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "topics_test")
    
    def test_transformational_vision(self):
        field_code = self.transformational_vision.code
        field_axis = self.transformational_vision.axis

        self.assertEquals(field_code, "00")
        self.assertEquals(field_axis, self.descarbonization_axis)
    
    def test_descarbonizador_axis(self):
        field_code = self.descarbonization_axis.code
        field_description = self.descarbonization_axis.description

        self.assertEquals(field_code, "00")
        self.assertEquals(field_description, "descarbonization_axis_test")
    
    def test_action_goal(self):
        field_code = self.action_goal.code
        field_area = self.action_goal.area

        self.assertEquals(field_code, "00")
        self.assertEquals(field_area, self.action_area)

    def test_action_area(self):
        field_code = self.action_area.code
        field_name = self.action_area.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "action_areas_test")
    
    def test_ghg_impact_sector(self):
        field_code = self.ghg_impact_sector.code
        field_name = self.ghg_impact_sector.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "ghg_impact_sector_test")

    def test_sustainable_dev_goals(self):
        field_code = self.sustainable_dev_goals.code
        field_description = self.sustainable_dev_goals.description

        self.assertEquals(field_code, "00")
        self.assertEquals(field_description, "sustainable_dev_goals_test_description")

    def test_impact_category(self):
        field_code = self.impact_category.code
        field_name = self.impact_category.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "impact_category_test")
    
    def test_carbon_deposit(self):
        field_code = self.carbon_deposit.code
        field_name = self.carbon_deposit.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "carbon_deposit_test")
    
    def test_standard(self):
        field_code = self.carbon_deposit.code
        field_name = self.carbon_deposit.name

        self.assertEquals(field_code, "00")
        self.assertEquals(field_name, "standard_test")
    
    def test_contact(self):
        
        field_institution = self.contact.institution
        field_full_name = self.contact.full_name
        field_job_title = self.contact.job_title
        field_email = self.contact.email
        field_phone = self.contact.phone
        
        self.assertEquals(field_institution, "institution test")
        self.assertEquals(field_full_name, "full_name test")
        self.assertEquals(field_job_title, "job_test")
        self.assertEquals(field_email, "email@email.com")
        self.assertEquals(field_phone, "88888888")
    
    def test_status(self):

        field_status = self.status.status
        field_code = self.status.code

        self.assertEquals(field_status, "status_test")
        self.assertEquals(field_code, "0")

    def finance_status_test(self):

        field_name = self.status.name
        field_code = self.status.code

        self.assertEquals(field_name, "finance_status")
        self.assertEquals(field_code, "00")
    
    def finance_source_test(self):

        field_name = self.status.name
        field_code = self.status.code

        self.assertEquals(field_name, "finance_source")
        self.assertEquals(field_code, "01")

    def geographic_scale_test(self):

        field_name = self.status.name
        field_code = self.status.code

        self.assertEquals(field_name, "geographic_scale")
        self.assertEquals(field_code, "02")
    
    def initiative_type_test(self):

        field_name = self.status.name
        field_code = self.status.code

        self.assertEquals(field_name, "initiative_type")
        self.assertEquals(field_code, "03")
    
    def finance_test(self):
        
        field_administration = self.finance.administration
        field_source_description = self.finance.source_description
        field_reference_year = self.finance.reference_year
        field_budget = self.finance.budget
        field_mideplan_project = self.finance.mideplan_project
        field_executed_entity = self.finance.exectuted_entity

        self.assertEquals(field_administration, "admin_test")
        self.assertEquals(field_source_description, "source_description")
        self.assertEquals(field_reference_year, 2000)
        self.assertEquals(field_budget, 1)
        self.assertEquals(field_mideplan_project, "mideplan_project_test")
        self.assertEquals(field_executed_entity, "exec_entity_test")

    def geographic_location_test(self):

        field_location = self.geographic_location.location

        self.assertEquals(field_location, "location_test")

    def initiative_test(self):

        field_name = self.initiative.name
        field_objetive = self.initiative.objetive
        field_description = self.initiative.description

        self.assertEquals(field_name, "name_initiative")
        self.assertEquals(field_objetive, "objetive_test")
        self.assertEquals(field_description, "description_test")

    def initiative_goal_test(self):

        field_goal = self.initiative_goal.goal

        self.assertEquals(field_goal, "goal_test")

    def mitigation_action_status_test(self):

        field_start_date = self.mitigation_action_status.start_date
        field_end_date = self.mitigation_action_status.end_date
        field_other_end_date = self.mitigation_action_status.other_end_date
        field_institution = self.mitigation_action_status.institution
        field_other_institution = self.mitigation_action_status.other_institution

        self.assertEquals(field_start_date, datetime.datetime(2007, 1, 1))
        self.assertEquals(field_end_date, datetime.datetime(2008, 1, 1))
        self.assertEquals(field_other_end_date, datetime.datetime(2009, 1, 1))
        self.assertEquals(field_institution, "institution_test_mitigation")
        self.assertEquals(field_other_institution, "other_institution_test")

    def ghg_insformation_test(self):


        field_impact_emission = self.ghg_information.impact_emission
        field_geographic_description = self.ghg_information.geographic_description

        self.assertEquals(field_impact_emission, "impact_emission_test")
        self.assertEquals(field_geographic_description, "geographic_description_test")
        