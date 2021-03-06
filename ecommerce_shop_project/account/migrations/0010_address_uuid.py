# Generated by Django 2.1.7 on 2019-05-08 17:56
import uuid
from django.db import migrations, models


def move_data_forwards(apps, schema_editor):
    Address = apps.get_model("account", "Address")
    for address in Address.objects.all():
        address.uuid = uuid.uuid4()
        address.save()


class Migration(migrations.Migration):

    dependencies = [("account", "0009_auto_20190507_2247")]

    operations = [
        migrations.AddField(
            model_name="address",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(move_data_forwards),
    ]
