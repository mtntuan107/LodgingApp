# Generated by Django 5.0.6 on 2024-05-23 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0007_lodging_title_alter_lodging_locate_alter_post_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentUL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lodging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_lodging', to='lodging.lodging')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_lodging', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]