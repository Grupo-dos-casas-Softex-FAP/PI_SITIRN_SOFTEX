# Generated by Django 5.1.3 on 2024-11-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webcrawler", "0005_alter_imovel_imovel_valor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imovel",
            name="imovel_valor",
            field=models.FloatField(),
        ),
    ]
