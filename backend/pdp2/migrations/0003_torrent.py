# Generated by Django 3.0.6 on 2020-10-05 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdp2', '0002_jsonstorage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_data_file', models.FileField(upload_to='development/torrent', verbose_name='File corresponding to torrent file')),
                ('info_hash', models.CharField(blank=True, max_length=64, null=True, verbose_name='Torrent info hash')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('file_uuid', models.CharField(default='99999999-9999-9999-9999-999999999999', max_length=36)),
            ],
        ),
    ]