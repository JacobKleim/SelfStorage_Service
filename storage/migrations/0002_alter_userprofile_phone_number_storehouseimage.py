# Generated by Django 4.2.13 on 2024-06-27 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=1),
        ),
        migrations.CreateModel(
            name='StorehouseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_pic', models.PositiveIntegerField(blank=True, db_index=True, default=0, verbose_name='Номер картинки')),
                ('img', models.ImageField(upload_to='', verbose_name='Картинка')),
                ('storehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='storage.storehouse', verbose_name='Склад')),
            ],
            options={
                'ordering': ['number_pic'],
            },
        ),
    ]
