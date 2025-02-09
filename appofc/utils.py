from PIL import Image
import io
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


def resize_image(photo):
    image = Image.open(photo)
    width, height = image.size

    # Automatically determine if the image is horizontal (landscape) or vertical (portrait)
    if width >= height:  # Horizontal (Landscape)
        min_width = 1920
        min_height = 1080
    else:  # Vertical (Portrait)
        min_width = 1080
        min_height = 1920

    # Check if the image meets the minimum resolution requirement
    if width < min_width or height < min_height:
        raise ValidationError(f"Image dimensions are too small. The minimum dimensions are {min_width}x{min_height}.")

    # If the image is larger than the allowed dimensions, resize it to fit within the max size
    max_width = 1920
    max_height = 1080
    if width > max_width or height > max_height:
        image.thumbnail((max_width, max_height), Image.LANCZOS)  # Resize keeping aspect ratio

    # Save the image in its original format (preserving quality)
    img_io = io.BytesIO()

    # Ensure the format is correctly set (handle 'JPG' as 'JPEG')
    image_format = photo.name.split('.')[-1].upper()
    if image_format == 'JPG':
        image_format = 'JPEG'

    if image_format not in ['JPEG', 'PNG', 'GIF', 'SVG',]:
        raise ValidationError("Unsupported file format.")
    
    image.save(img_io, format=image_format, quality=95)  # Save with high quality (95% quality for JPG)
    img_io.seek(0)

    # Create a temporary ContentFile from the resized image
    image_name = f"resized_{photo.name.rsplit('.', 1)[0]}.{image_format.lower()}"
    return ContentFile(img_io.read(), name=image_name)



