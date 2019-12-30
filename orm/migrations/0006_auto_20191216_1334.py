# Generated by Django 2.2.8 on 2019-12-16 13:34

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0005_auto_20191211_0519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('note', models.TextField(null=True)),
                ('status', models.CharField(choices=[('0', 'Tidak Hadir'), ('1', 'Hadir'), ('2', 'Izin')], default='0', max_length=50)),
                ('archery_range', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archery_range_precenses', to='orm.ArcheryRange')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_precenses', to='orm.ArcherMember')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisor_precenses', to='orm.ArcherMember')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Precense',
        ),
    ]
