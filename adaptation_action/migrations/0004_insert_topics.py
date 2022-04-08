from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_01 import _topics_data, _ndc_area, _adaptation_action_axis
from adaptation_action.models import Activity, AdaptationAxis, AdaptationAxisGuideline, NDCArea, NDCContribution, SubTopics, Topics

def insert_topics(apps, schema_editor):
    
    # Models
    Topics = apps.get_model('adaptation_action', 'Topics')
    SubTopics = apps.get_model('adaptation_action', 'SubTopics')
    Activity = apps.get_model('adaptation_action', 'Activity')
    NDCArea = apps.get_model('adaptation_action', 'NDCArea')
    NDCContribution = apps.get_model('adaptation_action', 'NDCContribution')
    AdaptationAxis = apps.get_model('adaptation_action', 'AdaptationAxis')
    AdaptationAxisGuideline = apps.get_model('adaptation_action', 'AdaptationAxisGuideline')

    for _data in _ndc_area:
        _ndc_contribution = _data.pop('ndc_contribution')
        ndc_area_record = NDCArea(**_data)
        ndc_area_record.save()

        for _ndc_contribution_data in _ndc_contribution:
            ndc_contribution_record = NDCContribution(ndc_area=ndc_area_record, **_ndc_contribution_data)
            ndc_contribution_record.save()

    for _data in _adaptation_action_axis:
        _adaptation_guidelines = _data.pop('guide_line')
        adaptation_axis_record = AdaptationAxis(**_data)
        adaptation_axis_record.save()

        for _adaptation_guideline_data in _adaptation_guidelines:
            adaptation_guideline_record = AdaptationAxisGuideline(adaptation_axis=adaptation_axis_record, **_adaptation_guideline_data)
            adaptation_guideline_record.save()

    for _data in _topics_data:
        _sub_topic = _data.pop('sub_topic')
        topic_record = Topics(**_data)
        topic_record.save()

        for sub_topic in _sub_topic:
            _activity = sub_topic.pop('activities')
            sub_topic_record = SubTopics(topic = topic_record, **sub_topic)
            sub_topic_record.save()

            
            for activity in _activity:
                _ndc = activity.pop('ndc_contribution', None)
                _axis = activity.pop('adaptation_axis', None)

                ndc_list = []
                if _ndc:
                    for ndc in _ndc:
                        parent_relation, child_relation = tuple(ndc.split('.'))
                        ndc_contribution = NDCContribution.objects.filter(code = child_relation, ndc_area__code = parent_relation).first()
                        ndc_list.append(ndc_contribution.id)
                    
                if _axis:
                    parent_relation, child_relation = tuple(_axis.split('.'))
                    axis = AdaptationAxisGuideline.objects.filter(code=child_relation, adaptation_axis__code=parent_relation).first()
                    activity['adaptation_axis_guideline'] = axis

                activity_record = Activity(sub_topic = sub_topic_record, **activity)
                activity_record.save()
                activity_record.ndc_contribution.add(*ndc_list)            


class Migration(migrations.Migration):
    
        dependencies = [
            ('adaptation_action', '0003_catalogs_adaptation'),
        ]
    
        operations = [
            migrations.RunPython(insert_topics),
        ]
