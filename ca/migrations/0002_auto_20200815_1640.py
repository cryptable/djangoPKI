# Generated by Django 3.1 on 2020-08-15 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='organizational_unit_name_text',
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizational_unit_1_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizational_unit_2_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizational_unit_3_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizational_unit_4_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizational_unit_5_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='ca',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ca.ca'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='country_code_text',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='generation_qualifier_text',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='given_name_text',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='initials_text',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='locality_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='organization_name_text',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='postal_code_text',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='private_key',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ca.privatekey'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='pseudonym_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='state_name_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='sur_name_text',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='title_text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
