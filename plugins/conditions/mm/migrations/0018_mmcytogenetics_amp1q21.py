from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0017_auto_20220923_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcytogenetics',
            name='amp1q21',
            field=models.CharField(
                blank=True,
                choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Unknown', 'Unknown')],
                max_length=10,
                null=True,
                verbose_name='amp 1q21',
            ),
        ),
    ]
