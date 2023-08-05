# Generated by Django 4.2.3 on 2023-07-30 22:05

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('ledger', '0005_alter_ingress_options_alter_purchase_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('fi', 'Suomi'), ('en', 'English'), ('es', 'Castellano'), ('ca', 'Català')], max_length=2)),
                ('name', models.CharField(max_length=100)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='taggit.tag')),
            ],
            options={
                'unique_together': {('tag', 'language')},
            },
        ),
        migrations.CreateModel(
            name='CustomTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug')),
                ('translations', models.ManyToManyField(blank=True, related_name='tags', to='ledger.tagtranslation')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
    ]
