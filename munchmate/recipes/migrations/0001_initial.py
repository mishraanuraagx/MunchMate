# Generated by Django 5.1.6 on 2025-03-06 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("recipe_type", models.IntegerField(default=0)),
                ("details", models.TextField()),
            ],
        ),
    ]
