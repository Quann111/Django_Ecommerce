# Generated by Django 5.0.1 on 2024-01-16 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='total_items',
            field=models.FloatField(default=0),
        ),
    ]
