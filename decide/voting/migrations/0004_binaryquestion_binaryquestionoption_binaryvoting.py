# Generated by Django 2.0 on 2022-11-13 08:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20180921_1119'),
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BinaryQuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('option', models.BooleanField(choices=[(1, 'De acuerdo'), (0, 'En desacuerdo')])),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.BinaryQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='BinaryVoting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tally', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('postproc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('auths', models.ManyToManyField(related_name='binaryvoting', to='base.Auth')),
                ('pub_key', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='binaryvoting', to='base.Key')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='binaryvoting', to='voting.BinaryQuestion')),
            ],
        ),
    ]
