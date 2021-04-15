# Generated by Django 3.0.6 on 2021-03-15 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.OAUTH2_PROVIDER_APPLICATION_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation', models.TextField(verbose_name='Recipient Representation')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thread_recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140, verbose_name='Thread Name')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('about', models.CharField(blank=True, max_length=140, null=True, verbose_name='Thread About')),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thread_owner', to=settings.AUTH_USER_MODEL)),
                ('recipients', models.ManyToManyField(to='pai_messages.ThreadRecipient')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(verbose_name='Body')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='sent at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Sender deleted at')),
                ('replied_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pai_messages.Message')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pai_messages.Thread')),
            ],
        ),
    ]