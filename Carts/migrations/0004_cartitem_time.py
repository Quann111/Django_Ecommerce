# Generated by Django 5.0.1 on 2024-01-16 06:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Carts', '0003_remove_cartitem_total_items_cart_total_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False),
        ),
    ]