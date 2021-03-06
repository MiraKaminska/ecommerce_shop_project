# Generated by Django 2.1.7 on 2019-03-27 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
