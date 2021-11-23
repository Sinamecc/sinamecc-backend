from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_01 import _topics_data
from adaptation_action.models import Activity, SubTopics, Topics

def insert_topics(apps, schema_editor):
    
    # Models
    Topics = apps.get_model('adaptation_action', 'Topics')
    SubTopics = apps.get_model('adaptation_action', 'SubTopics')
    Activity = apps.get_model('adaptation_action', 'Activity')

    for _data in _topics_data:
        _sub_topic = _data.pop('sub_topic')
        topic_record = Topics(**_data)
        topic_record.save()

        for sub_topic in _sub_topic:
            _activity = sub_topic.pop('activities')
            sub_topic_record = SubTopics(topic = topic_record, **sub_topic)
            sub_topic_record.save()

            for activity in _activity:
                activity_record = Activity(sub_topic = sub_topic_record, **activity)
                activity_record.save()


class Migration(migrations.Migration):
    
        dependencies = [
            ('adaptation_action', '0002_catalogs_adaptation'),
        ]
    
        operations = [
            migrations.RunPython(insert_topics),
        ]