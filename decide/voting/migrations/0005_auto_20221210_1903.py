# Generated by Django 2.0 on 2022-12-10 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20221207_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('Q', 'Question'), ('BQ', 'Binary Question'), ('SQ', 'Score Question')], default='Q', max_length=2),
        ),
        migrations.AddField(
            model_name='voting',
            name='voting_type',
            field=models.CharField(choices=[('V', 'Voting'), ('BV', 'Binary Voting'), ('SV', 'Score Voting')], default='V', max_length=2),
        ),
    ]
