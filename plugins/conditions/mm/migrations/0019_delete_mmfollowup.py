from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0018_mmdiagnosisdetails_amp1q21'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MMFollowUp',
        ),
    ]
