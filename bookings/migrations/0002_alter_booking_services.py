# Generated by Django 4.2.2 on 2023-07-14 19:49

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('homestays', '0005_alter_homestay_manager_id_and_more'),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='services',
            field=models.ManyToManyField(limit_choices_to={'homestay': django.db.models.expressions.OuterRef('homestay')}, to='homestays.service'),
        ),
    ]
