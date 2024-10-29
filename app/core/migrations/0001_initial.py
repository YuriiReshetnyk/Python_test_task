# Generated by Django 4.2.16 on 2024-10-25 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=36, unique=True)),
                ('password', models.CharField(max_length=31)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('avatar', models.URLField(max_length=255)),
                ('gender', models.CharField(max_length=31)),
                ('phone_number', models.CharField(max_length=50)),
                ('social_insurance_number', models.CharField(max_length=9)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_card_number', models.CharField(max_length=19)),
                ('credit_card_expiry_date', models.DateField()),
                ('credit_card_type', models.CharField(max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.externaluser')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('street_name', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('secondary_address', models.CharField(max_length=255)),
                ('building_number', models.CharField(max_length=255)),
                ('mail_box', models.CharField(max_length=255)),
                ('community', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('time_zone', models.CharField(max_length=255)),
                ('street_suffix', models.CharField(max_length=255)),
                ('city_suffix', models.CharField(max_length=255)),
                ('city_prefix', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('state_abbr', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('full_address', models.CharField(max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.externaluser')),
            ],
        ),
    ]