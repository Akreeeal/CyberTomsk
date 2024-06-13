# Generated by Django 4.2.1 on 2024-05-09 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('STD', 'STANDARD'), ('VIP', 'VIP'), ('BTC', 'BOOTCAMP'), ('PS5', 'PLAYSTATION')], max_length=4)),
                ('number', models.IntegerField(default=1)),
                ('processor', models.CharField(max_length=255)),
                ('ram', models.CharField(max_length=255)),
                ('graphics_card', models.CharField(max_length=255)),
                ('vram', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TempUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_session', models.DateTimeField()),
                ('stop_session', models.DateTimeField()),
                ('computer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.computer')),
            ],
        ),
    ]
