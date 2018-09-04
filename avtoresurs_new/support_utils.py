import os

from avtoresurs_new import settings


def get_brands_images_list():
    brands_path = 'static/main/images/brands/'
    brands_images_path = os.path.join(settings.BASE_DIR, brands_path)
    brands_images = os.listdir(
        brands_images_path
    )
    brands_images.sort()
    result = []
    for img in brands_images:
        result.append(
            os.path.join(os.sep, brands_path, img)
        )
    return result
