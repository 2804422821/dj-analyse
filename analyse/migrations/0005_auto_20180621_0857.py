# Generated by Django 2.0.6 on 2018-06-21 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0004_auto_20180612_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('last_update_user', models.IntegerField()),
                ('app', models.IntegerField()),
            ],
            options={
                'db_table': 'app_record',
            },
        ),
        migrations.CreateModel(
            name='AppRecordItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.IntegerField()),
                ('field', models.IntegerField()),
                ('field_value', models.TextField()),
            ],
            options={
                'db_table': 'app_record_item',
            },
        ),
        migrations.AlterField(
            model_name='field',
            name='default_show',
            field=models.BooleanField(default=True, verbose_name='默认是否显示'),
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.IntegerField(choices=[(1, '文本'), (2, '日期'), (3, '日期时间'), (4, '整数'), (5, '浮点数'), (6, '货币')], verbose_name='字段类型'),
        ),
    ]
