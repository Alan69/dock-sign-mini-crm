# Generated by Django 4.1.1 on 2024-05-12 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[(1, 'подписан'), (2, 'не подписан')], default='не подписан', max_length=20),
        ),
    ]
