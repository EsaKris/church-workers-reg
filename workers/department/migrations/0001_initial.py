# Generated by Django 5.1.3 on 2024-11-17 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(blank=True, max_length=4, unique=True)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(default='', max_length=15)),
                ('department', models.CharField(choices=[('Ushering', 'Ushering'), ('Sanctuary', 'Sanctuary'), ('Spirit and Truth', 'Spirit and Truth'), ('Technical', 'Technical'), ('Light and Power', 'Light and Power'), ('Labour Room', 'Labour Room'), ('New Wine Media', 'New Wine Media'), ('Decoration', 'Decoration'), ('Welfare', 'Welfare'), ('Pastoral Care', 'Pastoral Care')], default='New Wine Media', max_length=50)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
            ],
        ),
    ]
