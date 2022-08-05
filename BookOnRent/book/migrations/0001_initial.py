# Generated by Django 4.0.6 on 2022-08-01 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Author', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='')),
                ('quantity', models.IntegerField()),
                ('isbn_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RentedBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent', models.FloatField(default=0.0)),
                ('duration', models.IntegerField(default=1)),
                ('book_status', models.CharField(choices=[('ONRENT', 'onrent'), ('PENDING', 'pending'), ('PAID', 'paid'), ('RETURNED', 'returned')], default='ONRENT', max_length=20)),
                ('penalty', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
