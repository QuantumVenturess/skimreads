from django.conf import settings
from PIL import Image

import boto
import os
import PIL
import urllib
import urllib2

def delete_reading_image(reading):
    """
    Delete reading image on Amazon S3.
    """
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, 
            settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(settings.BUCKET_NAME)
    key = bucket.get_key('%s%s/%s_orig.jpg' % (
        settings.MEDIA_IMAGE_READ, reading.pk, reading.pk))
    if key:
        key.delete()

def set_reading_image(reading, url):
    """
    Retrieve image from url, crop, resize, upload, and remove.
    """
    name = '%s_orig' % reading.pk
    # ../media + / + img/reads/ + 1_orig + .jpg
    file_path = '%s%s.jpg' % (settings.MEDIA_IMAGE_READ_ROOT, name)
    absolute_path = file_path
    urllib.urlretrieve(url, file_path)
    #try:
    # retrieve image from url
    #urllib.urlretrieve(url, file_path)
    # crop image
    #crop_image(file_path, name)
    # resize image to 100x100
    #resize_image(file_path, 100.0, 100.0)
    # upload to amazon s3
    #upload_images(file_path, name, reading)
    # set reading.image
    #save_reading_image(name, reading)
    #except IOError:
        # URL does not exist
    #    pass

def crop_image(file_path, name):
    # Crop
    img = Image.open(file_path)
    width, height = img.size
    if width > height:
        left = int((width - height)/2.0)
        top = 0
        box = (left, top, left + height, top + height)
        img = img.crop(box)
    elif height > width:
        left = 0
        top = int((height - width)/2.0)
        box = (left, top, left + width, top + width)
        img = img.crop(box)
    try:
        os.remove(file_path)
    except WindowsError:
        pass
    img.save(file_path)

def resize_image(file_path, max_height, max_width):
    # Resize
    img = Image.open(file_path)
    width, height = img.size
    if width > max_width:
        img = img.resize((int(max_width), int(max_width)), 
            PIL.Image.ANTIALIAS)
    elif height > max_height:
        img = img.resize((int(max_height), int(max_height)), 
            PIL.Image.ANTIALIAS)
    try:
        os.remove(file_path)
    except WindowsError:
        pass
    img.save(file_path)

def upload_images(file_path, name, reading):
    # Upload
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, 
        settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(settings.BUCKET_NAME)
    key = bucket.new_key('%s%s/%s.jpg' % (
        settings.MEDIA_IMAGE_READ, reading.pk, name))
    key.set_contents_from_filename(file_path)
    key.set_acl('public-read')

def remove_images(reading):
    # Remove all images on the web server
    file_list = [f for f in os.listdir(
        settings.MEDIA_IMAGE_READ_ROOT) if f.startswith('%s_' % reading.pk)]
    for f in file_list:
        os.remove(settings.MEDIA_IMAGE_READ_ROOT + f)

def save_reading_image(name, reading):
    # Save reading image attribute
    reading.image = '%s%s/%s.jpg' % (settings.MEDIA_AWS_READ, 
        reading.pk, name)
    reading.save()

def reading_sort():
    """Key for sorting readings."""
    return lambda r: (r.month_day_year(), r.weight())

def reading_sorted(readings):
    """
    Return a list of readings that are sorted by date in reverse order.
    """
    return sorted(readings, 
        key=lambda r: (r.month_day_year(), r.weight()), reverse=True)