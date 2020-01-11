# Generated by Django 2.2.9 on 2020-01-11 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArcheryRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(null=True)),
                ('latitude', models.CharField(max_length=25)),
                ('longitude', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='BaseMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('full_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('pria', 'Pria'), ('wanita', 'Wanita')], max_length=10)),
                ('born_place', models.CharField(blank=True, max_length=45, null=True)),
                ('born_date', models.DateField(blank=True, null=True)),
                ('address', models.TextField()),
                ('date_register', models.DateField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, default='islam', max_length=45, null=True)),
                ('identity_card_number', models.CharField(blank=True, max_length=45, null=True)),
                ('identity_card_photo', models.ImageField(blank=True, null=True, upload_to='id_card/%Y/%m/%d')),
                ('blood_type', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=45, null=True)),
                ('disease_history', models.TextField(blank=True, default=None, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo/%Y/%m/%d')),
                ('public_photo', models.ImageField(blank=True, null=True, upload_to='public_photo/%Y/%m/%d')),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='qr_code/%Y/%m/%d')),
                ('skck', models.ImageField(blank=True, null=True, upload_to='skck/%Y/%m/%d')),
                ('status', models.CharField(blank=True, choices=[('1', 'Menunggu Persetujuan'), ('2', 'Diterima'), ('3', 'Ditolak')], default='1', max_length=10, null=True)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('date_register', models.DateField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/club/%Y/%m/%d')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubs', to='orm.Branch')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Periode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_periode', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_height', models.CharField(blank=True, default='0', max_length=25, null=True)),
                ('body_weight', models.CharField(blank=True, default='0', max_length=25, null=True)),
                ('draw_length', models.CharField(blank=True, default='0', max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticeContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('target_type', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=25, null=True)),
                ('longitude', models.CharField(blank=True, max_length=25, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('distance', models.FloatField(default=1)),
                ('series', models.IntegerField(default=1)),
                ('arrow', models.IntegerField(default=1)),
                ('status', models.CharField(blank=True, choices=[('0', 'Waiting'), ('1', 'Rejected'), ('3', 'Approved')], default='0', max_length=50, null=True)),
                ('signed', models.BooleanField(blank=True, default=False, null=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('archery_range', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='practices', to='orm.ArcheryRange')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='practices', to='orm.BaseMember')),
                ('signed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signed_practices', to='orm.BaseMember')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PresenceContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255)),
                ('latitude', models.CharField(blank=True, max_length=25, null=True)),
                ('longitude', models.CharField(blank=True, max_length=25, null=True)),
                ('closed', models.BooleanField(blank=True, default=False)),
                ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_presence', to='orm.Club')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator_presence', to='orm.BaseMember')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TargetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('achievement', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOutItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('unit', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOutTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('target', models.IntegerField(default=0)),
                ('unit', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wo_targets', to='orm.WorkOutItem')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wo_targets', to='orm.BaseMember')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOutContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('finished', models.BooleanField(default=False)),
                ('workouts', models.ManyToManyField(related_name='wo_containers', to='orm.WorkOut')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='workout',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workouts', to='orm.WorkOutItem'),
        ),
        migrations.AddField(
            model_name='workout',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workouts', to='orm.BaseMember'),
        ),
        migrations.AddField(
            model_name='workout',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workouts', to='orm.WorkOutTarget'),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('date_register', models.DateField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/unit/%Y/%m/%d')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='units', to='orm.Branch')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('regional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provinces', to='orm.Region')),
            ],
        ),
        migrations.CreateModel(
            name='PresenceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('note', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('0', 'Tidak Hadir'), ('1', 'Hadir'), ('2', 'Izin')], default='0', max_length=50)),
                ('container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='presence_items', to='orm.PresenceContainer')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_presence', to='orm.BaseMember')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisor_presence', to='orm.BaseMember')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='presencecontainer',
            name='satuan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='satuan_presence', to='orm.Unit'),
        ),
        migrations.CreateModel(
            name='PracticeSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('serie', models.IntegerField(default=0)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='practice/sk/%Y/%m/%d')),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('practice_container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice_series', to='orm.PracticeContainer')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PracticeScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='orm.PracticeSeries')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('username', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, choices=[('1', 'Menunggu Persetujuan'), ('2', 'Diterima'), ('3', 'Ditolak')], default='1', max_length=10, null=True)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='change_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='branch',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branchs', to='orm.Province'),
        ),
        migrations.CreateModel(
            name='Bow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bows', to='orm.BaseMember')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='basemember',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='orm.Club'),
        ),
        migrations.AddField(
            model_name='basemember',
            name='physic_information',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orm.PhysicInformation'),
        ),
        migrations.AddField(
            model_name='basemember',
            name='satuan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='orm.Unit'),
        ),
        migrations.AddField(
            model_name='basemember',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Arrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrows', to='orm.BaseMember')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='archeryrange',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archery_ranges', to='orm.Club'),
        ),
        migrations.AddField(
            model_name='archeryrange',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archery_ranges', to='orm.Unit'),
        ),
        migrations.CreateModel(
            name='RegionalCommiteMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orm.BaseMember')),
                ('position', models.CharField(max_length=100)),
                ('sk_number', models.CharField(blank=True, max_length=100, null=True)),
                ('sk_document', models.FileField(blank=True, null=True, upload_to='docs/sk/%Y/%m/%d')),
                ('periode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Periode')),
                ('regional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Region')),
            ],
            options={
                'abstract': False,
            },
            bases=('orm.basemember',),
        ),
        migrations.CreateModel(
            name='PengprovCommiteMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orm.BaseMember')),
                ('position', models.CharField(max_length=100)),
                ('sk_number', models.CharField(blank=True, max_length=100, null=True)),
                ('sk_document', models.FileField(blank=True, null=True, upload_to='docs/sk/%Y/%m/%d')),
                ('periode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Periode')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Province')),
            ],
            options={
                'abstract': False,
            },
            bases=('orm.basemember',),
        ),
        migrations.CreateModel(
            name='PengcabCommiteMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orm.BaseMember')),
                ('position', models.CharField(max_length=100)),
                ('sk_number', models.CharField(blank=True, max_length=100, null=True)),
                ('sk_document', models.FileField(blank=True, null=True, upload_to='docs/sk/%Y/%m/%d')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Branch')),
                ('periode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Periode')),
            ],
            options={
                'abstract': False,
            },
            bases=('orm.basemember',),
        ),
        migrations.CreateModel(
            name='ClubUnitCommiteMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orm.BaseMember')),
                ('position', models.CharField(max_length=100)),
                ('sk_number', models.CharField(blank=True, max_length=100, null=True)),
                ('sk_document', models.FileField(blank=True, null=True, upload_to='docs/sk/%Y/%m/%d')),
                ('periode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orm.Periode')),
            ],
            options={
                'abstract': False,
            },
            bases=('orm.basemember',),
        ),
        migrations.CreateModel(
            name='ArcherMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orm.BaseMember')),
                ('verified', models.BooleanField(blank=True, default=False, null=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_approval', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
            bases=('orm.basemember',),
        ),
    ]
