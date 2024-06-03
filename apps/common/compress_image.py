import mimetypes
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class MediaService(object):
    def compress_media(self, field, delete_source=False, max_size=1024 * 1024 * 10, max_width=1200, max_height=1080):
        media_file = getattr(self, field)

        # Получаем тип содержимого файла
        content_type, _ = mimetypes.guess_type(media_file.name)

        # Если файл является изображением
        if content_type.startswith("image"):
            self._compress_image(
                field=field,
                delete_source=delete_source,
                max_width=max_width,
                max_height=max_height,
            )
        # Если файл является видео
        elif content_type.startswith("video"):
            self._compress_video(
                field=field,
                delete_source=delete_source,
                max_size=max_size,
            )

    def _compress_image(self, field, delete_source, max_width, max_height):
        image = getattr(self, field)
        img = Image.open(image)
        img_width, img_height = img.size
        if img.mode != "RGB":
            img = img.convert("RGB")
        if image and (img_width > max_width or img_height > max_height):
            width = img_width if img_width < max_width else max_width
            height = img_height if img_height < max_height else max_height
            img.thumbnail((width, height), Image.LANCZOS)
        output = BytesIO()
        img.save(output, format="JPEG", quality=70, optimize=True, progressive=True)
        output.seek(0)
        new_image = InMemoryUploadedFile(
            output, "ImageField", f"{image.name.split('.')[0]}.jpg", "image/jpeg", sys.getsizeof(output), None
        )
        if delete_source:
            image.delete(False)
        setattr(self, field, new_image)

    def _compress_video(self, field, delete_source, max_size):
        pass
