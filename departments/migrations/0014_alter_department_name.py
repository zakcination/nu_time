# Generated by Django 4.2.9 on 2024-02-03 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0013_alter_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(choices=[('SMG', 'SMG | School of Mining and Geosciences'), ('NUSOM', 'NUSOM | School of Medicine'), ('GSB', 'GSB | Graduate School of Business'), ('GSE', 'GSE | Graduate School of Education'), ('SSH', 'SSH | School of Sciences and Humanities'), ('GSPP', 'GSPP | Graduate School of Public Policy'), ('SEDS', 'SEDS | School of Engineering and Digital Sciences'), ('CPS', 'CPS | Center for Preparatory Studies')], max_length=6, unique=True),
        ),
    ]
