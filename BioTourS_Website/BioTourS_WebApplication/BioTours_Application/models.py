import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.formats import date_format
from django.core.exceptions import ValidationError


class Prevalent_Behavior(models.Model):
    Behavior = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Prevalent_Behavior'
        verbose_name_plural = 'Prevalent_Behaviors'
        db_table = 'Prevalent_Behavior'

    def __str__(self):
        return self.Behavior


class Research_Activity(models.Model):
    Activity = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Research_Activity'
        verbose_name_plural = 'Research_Activities'
        db_table = 'Research_Activity'

    def __str__(self):
        return self.Activity


class Dolphin_Species(models.Model):
    Name_Species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Dolphin_Species'
        verbose_name_plural = 'Dolphin_Species'
        db_table = 'Dolphin_Species'

    def __str__(self):
        return self.Name_Species


def validate_longitude(value):
    if abs(value) <= 180:
        return value
    else:
        raise ValidationError("Longitude MUST BE in the range [ -180, 180 ]")


def validate_latitude(value):
    if abs(value) <= 90:
        return value
    else:
        raise ValidationError("Latitude MUST BE in the range [ -90, 90 ]")


class Sighting(models.Model):
    Port = models.CharField(max_length=100, default="Not available")
    Date = models.DateField(help_text='Date Format: YYYY-MM-DD', )
    Start_Activity_Time = models.TimeField(blank=True, null=True, help_text='Time Format: HH:mm:ss')
    End_Activity_Time = models.TimeField(blank=True, null=True)
    Start_Contact_Time = models.TimeField(blank=True, null=True)
    End_Contact_Time = models.TimeField(blank=True, null=True)
    Latitude_Contact = models.FloatField(blank=True, null=True,
                                         validators=[validate_latitude],
                                         help_text='The Equator has a latitude of 0°, the North Pole has a '
                                                   'latitude of 90° North (+90°), and the '
                                                   'South Pole has a latitude of 90° South (−90°). ')

    Longitude_Contact = models.FloatField(blank=True, null=True,
                                          validators=[validate_longitude],
                                          help_text='Longitude is given as an angular measurement ranging from 0° at'
                                                    ' the Prime Meridian to +180° eastward and −180° westward.')

    Depth = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    First_Species_Observed = models.ForeignKey(Dolphin_Species, on_delete=models.DO_NOTHING, blank=True, null=True)
    Second_Species_Observed = models.ManyToManyField(Dolphin_Species, related_name="Second_Species_Observed")
    Number_Individuals = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    Number_Calves = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Number of small dolphins',
                                                     default=0)
    Behavior = models.ManyToManyField(Prevalent_Behavior)
    Activity = models.ManyToManyField(Research_Activity)
    Other_Boats = models.CharField(max_length=100, blank=True, null=True, default="Not available")
    Fishing_Gear_Available = models.CharField(max_length=100, blank=True, null=True, default="Not available")
    Interaction_With_Gear = models.CharField(max_length=100, blank=True, null=True, default="Not available")
    Other_Organism = models.CharField(max_length=100, blank=True, null=True, default="Not available")
    Notes = models.TextField(blank=True, null=True, default="Not available")

    class Meta:
        verbose_name = 'Sighting'
        verbose_name_plural = 'Sightings'
        db_table = 'Sighting'

    # ToString method of Sighting class, which return Port and date of sighting
    def __str__(self):
        return self.Port + '_' + date_format(self.Date)

    # Return a string with the list of research activities
    def list_of_research_activities(self):
        list_activities = ', '.join([str(act) for act in self.Activity.all()])
        if len(list_activities) <= 0:
            list_activities = '-'
        return list_activities

    # Return a string with the list of prevalent behaviors
    def list_of_prevalent_behaviors(self):
        list_behaviors = ', '.join([str(behavior) for behavior in self.Behavior.all()])
        if len(list_behaviors) <= 0:
            list_behaviors = '-'
        return list_behaviors


def get_upload_path(instance, filename):
    fk = instance.sighting.pk
    path = str(fk) + '_' + str(Sighting.objects.get(pk=fk)).replace(' ', '_').replace(',', '')
    absolute_p = '%s/%s' % (path, filename)
    return absolute_p


class File_Sighting(models.Model):
    file = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(['mp4', 'jpg', 'png', 'jpeg',
                                                                                           'HEIC'])])
    sighting = models.ForeignKey(Sighting, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Sighting_File'
        verbose_name_plural = 'Sighting_Files'
        db_table = 'Sighting_File'

    def __str__(self):
        # Retrieve the related sighting of each file
        sighting_obj = Sighting.objects.get(pk=self.sighting.pk)
        # return the port and date
        return str(sighting_obj)

    def save(self, *args, **kwargs):
        if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            im = Image.open(self.file)
            output = BytesIO()

            original_width, original_height = im.size
            aspect_ratio = round(original_width / original_height)
            desired_height = 800  # Edit to add your desired height in pixels
            desired_width = desired_height * aspect_ratio

            im = im.resize((desired_width, desired_height))
            im.save(output, format='JPEG', quality=90)

            self.file = InMemoryUploadedFile(output, 'FileField', "%s.jpg" % self.file.name.split('.')[0], 'image/jpeg',
                                             sys.getsizeof(output), None)

            super(File_Sighting, self).save(*args, **kwargs)
