# Generated by Django 2.0.2 on 2019-02-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0007_auto_20190226_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivos',
            name='archivo',
            field=models.FileField(upload_to='documentos/'),
        ),
    ]
