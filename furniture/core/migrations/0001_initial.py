# Generated by Django 5.1.7 on 2025-05-06 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='category_icons/')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('customer', 'Customer'), ('furnisher', 'Furnisher'), ('consultant', 'Consultant')], max_length=20)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bio', models.TextField(blank=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('available_rn', models.CharField(choices=[('available', 'Available'), ('not_available', 'Not Available')], default='available', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('category', models.ManyToManyField(blank=True, related_name='goods', to='core.category')),
                ('furnishers', models.ManyToManyField(blank=True, related_name='furnishers', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.CharField(choices=[('not_needed', 'Not Needed'), ('standart', 'Standart'), ('express', 'Express')], max_length=20)),
                ('date_of_purchase', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultant', to='core.profile')),
                ('customer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='core.profile')),
                ('list_of_goods', models.ManyToManyField(blank=True, related_name='list', to='core.goods')),
            ],
        ),
    ]
