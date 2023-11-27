# Generated by Django 4.2.6 on 2023-11-24 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Spot', '0007_rename_reserves_reserve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='currency_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_currency', to='Spot.digitalcurrency'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='spot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_spot', to='Spot.spot'),
        ),
    ]
