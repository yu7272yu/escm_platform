# Generated by Django 3.2.13 on 2022-12-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfomodel',
            name='create_time',
            field=models.IntegerField(default=1669977558),
        ),
        migrations.AlterField(
            model_name='userinfomodel',
            name='update_time',
            field=models.IntegerField(default=1669977558, verbose_name='最后更新时间'),
        ),
        migrations.AlterField(
            model_name='userrolemodel',
            name='create_time',
            field=models.IntegerField(default=1669977558),
        ),
        migrations.AlterField(
            model_name='userrolemodel',
            name='update_time',
            field=models.IntegerField(default=1669977558, verbose_name='最后更新时间'),
        ),
    ]
