import datetime
import pathlib
import sys

from django.conf import settings
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from carbondoomsday.measurements.models import CO2

ppm = sys.argv[1]


def add_border_radius(im, rad):
    """
    Via https://stackoverflow.com/a/11291419/2532070
    """
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def create_email_signature(ppm):
    """
    Utility function for creating an email signature PNG using Pillow.

    Inspiration from:
    https://code-maven.com/create-images-with-python-pil-pillow
    https://stackoverflow.com/a/38629258/2532070
    https://stackoverflow.com/a/273962/2532070
    https://stackoverflow.com/a/2563883/2532070
    """
    ppm = str(ppm)
    img = Image.new('RGB', (200, 70), color="#FF5964")

    large_font = ImageFont.truetype(
        settings.BASE_DIR +
        '/carbondoomsday/email_signature/ProximaNova-Bold.otf',
        24)
    small_font = ImageFont.truetype(
        settings.BASE_DIR +
        '/carbondoomsday/email_signature/ProximaNova-Bold.otf',
        12)

    size = 16, 16
    skull_image = Image.open('carbondoomsday/email_signature/skull.png', 'r')
    skull_image.thumbnail(size, Image.ANTIALIAS)

    d = ImageDraw.Draw(img)
    d.text((15, 10), ppm, font=large_font, fill="#FFF")
    d.text((103, 20), "PPM", font=small_font, fill="#FFB3B8")
    d.text((140, 10), "CO", font=large_font, fill="#FFF")
    d.text((175, 30), "2", font=small_font, fill="#FFF")
    date = datetime.date.today().strftime('%m/%d')
    d.text(
        (35, 44),
        "CarbonDoomsday {}".format(date),
        font=small_font,
        fill="#FFB3B8"
    )

    img.paste(skull_image, (15, 42), mask=skull_image)

    img = add_border_radius(img, 15)

    enhancer = ImageEnhance.Sharpness(img)

    directory = './mediafiles'
    pathlib.Path(directory).mkdir(exist_ok=True)

    enhancer.enhance(2.0).save('mediafiles/carbondoomsday_email_signature.png')


def update_email_signature():
    co2_measurement = CO2.objects.latest('created')
    create_email_signature(co2_measurement.ppm)
