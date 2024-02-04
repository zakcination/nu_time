# Generated by Django 4.2.9 on 2024-02-03 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0005_alter_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(choices=[('SMG', 'School of Mining and Geosciences'), ('GSPP', 'Graduate School of Public Policy'), ('GSB', 'Graduate School of Business'), ('CPS', 'Center for Preparatory Studies'), ('SSH', 'School of Sciences and Humanities'), ('GSE', 'Graduate School of Education'), ('SEDS', 'School of Engineering and Digital Sciences'), ('NUSOM', 'School of Medicine')], default='SEDS', max_length=50),
        ),
    ]