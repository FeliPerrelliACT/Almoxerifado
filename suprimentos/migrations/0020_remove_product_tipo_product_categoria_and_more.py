# Generated by Django 5.2 on 2025-04-17 13:13

import django.db.models.deletion
import django.db.models.query
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suprimentos', '0019_centrocusto_data_inativacao_alter_request_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tipo',
        ),
        migrations.AddField(
            model_name='product',
            name='categoria',
            field=models.CharField(choices=[('ferramenta', 'Ferramenta'), ('epi', 'EPI'), ('material', 'Material')], default='ferramenta', max_length=20),
        ),
        migrations.AlterField(
            model_name='request',
            name='created_by',
            field=models.ForeignKey(default=django.db.models.query.QuerySet.first, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
