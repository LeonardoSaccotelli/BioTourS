# Register your models here.
import io
import zipfile
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.gis.db.models import PointField
from django.contrib.gis.forms import OSMWidget
from django.db.models import DateField, TimeField
from django.http import HttpResponse
from import_export.admin import ImportExportMixin
from .forms import DateInput, TimeInput
from .models import Prevalent_Behavior, Research_Activity, Dolphin_Species, Sighting, File_Sighting, Gallery
from .resources import SightingResource


# Removed 'Group' from admin section
admin.site.unregister(Group)

# Change header name in the administration section
admin.site.site_header = 'BioTourS Admin Dashboard'

# Change title name of site
admin.site.site_title = 'BioTourS Admin Dashboard'

admin.site.index_title = ''

# Corresponding to the tab 'View Site'
admin.site.site_url = ''


# Create a TabularInline to enter one or more Secondary Species observed
class DolphinSecondSpeciesSightingInline(admin.TabularInline):
    model = Sighting.Second_Species_Observed.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Secondary Species Observed'
    verbose_name_plural = 'Secondary Species Observed'


class DolphinSpeciesModelAdmin(admin.ModelAdmin):
    list_per_page = 15


# Create a TabularInline to enter one or more Prevalent Behavior observed
class PrevalentBehaviorSightingInline(admin.TabularInline):
    model = Sighting.Behavior.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Prevalent Behavior'
    verbose_name_plural = 'Prevalent Behaviors'


class PrevalentBehaviorModelAdmin(admin.ModelAdmin):
    list_per_page = 15


# Create a TabularInline to enter one or more Research Activities
class ResearchActivitySightingInline(admin.TabularInline):
    model = Sighting.Activity.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Research Activity'
    verbose_name_plural = 'Research Activities'


class ResearchActivityModelAdmin(admin.ModelAdmin):
    list_per_page = 15


# Create a TabularInline to enter one or more Images
class FileSightingInline(admin.TabularInline):
    model = File_Sighting
    extra = 0
    classes = ['collapse']
    verbose_name = 'Sighting File'
    verbose_name_plural = 'Sighting Files'


@admin.action(description='Download files associated with the selected Sightings')
def download_files(modeladmin, request, queryset):
    byte_data = io.BytesIO()
    zip_file = zipfile.ZipFile(byte_data, "w")

    for sighting_obj in queryset:
        filelist = [file_sighting.file
                    for file_sighting in File_Sighting.objects.filter(sighting=sighting_obj.pk)]

        for file in filelist:
            zip_file.write(file.path, str(file))
    zip_file.close()

    response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=sighting_files.zip'

    # Print list files in zip_file
    zip_file.printdir()

    return response


# Define a layout for Sighting field, grouping in different fieldset
class SightingAdmin(ImportExportMixin, admin.ModelAdmin):
    # Divide fields in fieldsets

    resource_class = SightingResource

    fieldsets = [
        ('Location Information', {'fields': ['Port', 'Latitude_Contact', 'Longitude_Contact', 'Gps_Location'],
                                  'classes': ('collapse',)
                                  }),
        ('Date and time information', {'fields': ['Date', 'Start_Activity_Time',
                                                  'End_Activity_Time',
                                                  'Start_Contact_Time', 'End_Contact_Time'],
                                       'classes': ('collapse',)
                                       }),
        ('Dolphin Information', {'fields': ['First_Species_Observed', 'Depth', 'Number_Individuals', 'Number_Calves', ],
                                 'classes': ('collapse',)
                                 }),

        ('Other Information', {'fields': ['Other_Boats', 'Fishing_Gear_Available', 'Interaction_With_Gear',
                                          'Other_Organism', 'Notes'],
                               'classes': ('collapse',)
                               })
    ]

    # Select fields to be shown in table
    list_display = ('Port', 'Date', 'First_Species_Observed',
                    'Number_Individuals', 'list_of_research_activities', 'list_of_prevalent_behaviors')

    formfield_overrides = {
        PointField: {"widget": OSMWidget},
        DateField: {"widget": DateInput},
        TimeField: {"widget": TimeInput},
    }

    # Sort by date
    ordering = ['Date']

    # Add a list of filter
    list_filter = ('Date', 'First_Species_Observed', 'Behavior', 'Activity')

    # Add a search field by 'Port','Date', 'First_Species_observed'
    search_fields = ('Port',)

    # Insert a link on field
    list_display_links = ['Port']

    inlines = [DolphinSecondSpeciesSightingInline,
               PrevalentBehaviorSightingInline, ResearchActivitySightingInline,
               FileSightingInline]

    actions = [download_files]

    list_per_page = 15


class GalleryModelAdmin(admin.ModelAdmin):
    list_per_page = 15


# Register the model data for admin section
admin.site.register(Sighting, SightingAdmin)
admin.site.register(Prevalent_Behavior, PrevalentBehaviorModelAdmin)
admin.site.register(Research_Activity, ResearchActivityModelAdmin)
admin.site.register(Dolphin_Species, DolphinSpeciesModelAdmin)
admin.site.register(Gallery, GalleryModelAdmin)
