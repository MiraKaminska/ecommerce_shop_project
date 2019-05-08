# Generated by Django 2.1.7 on 2019-04-24 17:57

from django.db import migrations, models
import django.db.models.deletion


def rename_fields_forwards(apps, schema_editor):
    apps.get_model("shop", "ProductImage")


def rename_fields_backwards(apps, schema_editor):
    apps.get_model("shop", "ProductImage")


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_merge_20190422_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', upload_to='images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.Product')),
            ],
        ),
        migrations.RunPython(rename_fields_forwards, rename_fields_backwards),
    ]
