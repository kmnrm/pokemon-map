# Generated by Django 2.2.5 on 2020-02-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='img_url',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Изображение покемона'),
        ),
    ]