# Generated by Django 2.0 on 2022-11-14 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='type',
            field=models.CharField(choices=[('V', 'Voting'), ('BV', 'BinaryVoting'), ('MV', 'MultipleVoting'), ('SV', 'ScoreVoting')], default='V', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='census',
            unique_together={('voting_id', 'voter_id', 'type')},
        ),
    ]