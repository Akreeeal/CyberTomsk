# Generated by Django 4.2.1 on 2024-05-27 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_review_delete_tempuser_computer_hours_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
