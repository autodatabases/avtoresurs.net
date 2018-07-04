import uuid
import os

from avtoresurs_new.settings import MEDIA_ROOT, MEDIA_URL


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{name}.{ext}".format(name=uuid.uuid4(), ext=ext)
    return os.path.join(filename)
