# Generated by Django 3.0.4 on 2020-03-15 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(blank=True, default=0.0)),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('own_hash', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('nonce', models.IntegerField(blank=True, default=0)),
                ('prev_hash', models.CharField(blank=True, max_length=255)),
                ('merkle_root', models.CharField(blank=True, max_length=255)),
                ('high', models.IntegerField(default=0, null=True)),
                ('own_hash', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('difficult', models.PositiveIntegerField(default=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_account', models.CharField(blank=True, max_length=255)),
                ('quantity', models.FloatField(blank=True, default=0)),
                ('to_account', models.CharField(blank=True, max_length=255)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apiblockchain.Block')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='header',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apiblockchain.Header'),
        ),
    ]
