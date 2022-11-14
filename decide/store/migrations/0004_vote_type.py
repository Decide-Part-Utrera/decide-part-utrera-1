# Generated by Django 2.0 on 2022-11-14 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20180921_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='type',
            field=models.CharField(choices=[('V', 'Voting'), ('BV', 'BinaryVoting'), ('MV', 'MultipleVoting'), ('SV', 'ScoreVoting')], default='V', max_length=2),
        ),
    ]
