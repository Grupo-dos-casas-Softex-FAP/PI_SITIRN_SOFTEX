# Generated by Django 5.1.3 on 2024-11-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webcrawler", "0004_alter_imovel_imovel_valor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imovel",
            name="imovel_valor",
            field=models.CharField(max_length=100),
        ),
    ]
