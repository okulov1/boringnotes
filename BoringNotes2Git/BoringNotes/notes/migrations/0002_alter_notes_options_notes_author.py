# Generated by Django 4.2.3 on 2023-07-20 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'verbose_name': 'Заметка', 'verbose_name_plural': 'Заметки'},
        ),
        migrations.AddField(
            model_name='notes',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]