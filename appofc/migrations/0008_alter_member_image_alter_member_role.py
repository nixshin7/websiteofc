# Generated by Django 5.1.4 on 2025-02-03 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appofc', '0007_alter_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(max_length=100),
        ),
    ]
