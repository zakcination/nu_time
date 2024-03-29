# Generated by Django 4.2.9 on 2024-01-28 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_alter_department_name_and_more'),
        ('courses', '0002_coursegetting_grade_distribution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='credits',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(default='Simple department', on_delete=django.db.models.deletion.CASCADE, to='departments.department'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(default='Simple description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='coursegetting',
            name='capacity',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='coursegetting',
            name='grade',
            field=models.CharField(choices=[('B+', 'B+'), ('I', 'I'), ('A-', 'A-'), ('P', 'P'), ('AU', 'AU'), ('D+', 'D+'), ('C-', 'C-'), ('A', 'A'), ('D', 'D'), ('C', 'C'), ('W', 'W'), ('C+', 'C+'), ('F', 'F'), ('B-', 'B-'), ('B', 'B')], default='A', max_length=2),
        ),
        migrations.AlterField(
            model_name='coursegetting',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.instructor'),
        ),
        migrations.AlterField(
            model_name='coursegetting',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.semester'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('course', 'section_number')},
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('start_from', 'end_at', 'name')},
        ),
    ]
