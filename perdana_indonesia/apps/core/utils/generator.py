from io import BytesIO

import qrcode
from django.core.files.base import ContentFile


def generate_qrcode_from_text(value):
    im_qrcode = qrcode.make(value)
    img_io = BytesIO()
    im_qrcode.save(img_io, format='PNG', quality=100)
    img_content = ContentFile(img_io.getvalue(), '%s.png' % value)
    return img_content
