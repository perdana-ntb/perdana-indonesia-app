PERDANA_USER_ROLE_CHOICES = (
    ('pusat', 'Pengurus Pusat'),
    ('pengprov', 'Pengurus Provinsi (DPD)'),
    ('pengcab', 'Pengurus Kabupaten (DPC)'),
    ('puslat-manager', 'Pengurus Puslat'),
    ('archer', 'Pemanah')
)

CHANGE_STATUS_CHOICES = (
    ('1', 'Menunggu Persetujuan'),
    ('2', 'Diterima'),
    ('3', 'Ditolak'),
)

GENDER_CHOICES = (
    ('Pria', 'Pria'),
    ('Wanita', 'Wanita')
)

BLOOD_TYPE_CHOICES = (
    ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')
)

RELIGION_CHOICES = (
    ('islam', 'Islam'),
)

CLUB_UNIT_TYPE_CHOICES = (
    ('club', 'Club'),
    ('satuan', 'Satuan')
)

PRESENCE_STATUS_CHOICES = (
    ('0', 'Tidak Hadir'),
    ('1', 'Hadir'),
    ('2', 'Izin'),
)

PRACTICE_STATUS_CHOICES = (
    ('0', 'Waiting'),
    ('1', 'Rejected'),
    ('3', 'Approved'),
)
