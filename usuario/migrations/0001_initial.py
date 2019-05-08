# Generated by Django 2.2 on 2019-05-08 06:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import usuario.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RFC', models.CharField(max_length=15, null=True)),
                ('tipo_persona', models.CharField(max_length=15, null=True)),
                ('razon_social', models.CharField(max_length=100, null=True, unique=True)),
                ('direccion_fiscal', models.CharField(max_length=125, null=True)),
                ('e_firma_key', models.FileField(null=True, upload_to=usuario.models.upload_e_firma)),
                ('e_firma_cer', models.FileField(null=True, upload_to=usuario.models.upload_e_firma)),
                ('clave_privada', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
                ('ciec', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
                ('contador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contador_personal', to='administrador.Administrador')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('is_user', 'Is_User'),),
            },
        ),
        migrations.CreateModel(
            name='PagoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('referencia', models.CharField(max_length=100, null=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargo_a_usuario', to='usuario.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subido_el', models.DateTimeField(auto_now_add=True)),
                ('xml', models.FileField(upload_to=usuario.models.upload_factura)),
                ('pdf', models.FileField(upload_to=usuario.models.upload_factura)),
                ('fecha', models.DateTimeField(null=True)),
                ('tipo', models.CharField(max_length=1, null=True)),
                ('RFC', models.CharField(max_length=14, null=True)),
                ('razon_social', models.CharField(max_length=100, null=True)),
                ('vigente', models.BooleanField(default=True)),
                ('sub_total', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
                ('contador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contadorACargo', to='administrador.Administrador')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FDI', to='usuario.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=200, null=True)),
                ('razon_social', models.CharField(max_length=200, null=True)),
                ('direccion', models.CharField(max_length=200, null=True)),
                ('RFC', models.CharField(max_length=10, null=True)),
                ('contador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_personal', to='usuario.Usuario')),
            ],
        ),
    ]
