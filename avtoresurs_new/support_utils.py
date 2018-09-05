import os

from avtoresurs_new import settings


def get_brands_images_list():
    brands_path = '/main/images/brands/'
    brands_images_path = "%s%s" % (settings.STATICFILES_DIRS[0], brands_path)
    brands_images = os.listdir(
        brands_images_path
    )
    brands_images.sort()
    result = []
    for img in brands_images:
        result.append(
            "/media/{img_name}".format(
                img_name=img
            )
        )
    return result
