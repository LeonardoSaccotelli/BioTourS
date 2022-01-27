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


@admin.action(description='Download selected files')
def download_files(modeladmin, request, queryset):
    zip_filename = 'sighting_files.zip'
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_STORED, False) as zip_file:
        for obj in queryset:
            path_file = obj.file
            zip_file.writestr(str(path_file), path_file.path)
    zip_buffer.seek(0)
    resp = HttpResponse(zip_buffer, content_type='application/zip')
    resp['Content-Disposition'] = 'attachment; filename = %s' % zip_filename
    return resp


class FileSightingModelAdmin(admin.ModelAdmin):
    actions = [download_files]


# Create a TabularInline to enter one or more Secondary Species observed
class DolphinSecondSpeciesSightingInline(admin.TabularInline):
    model = Sighting.Second_Species_Observed.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Secondary Species Observed'
    verbose_name_plural = 'Secondary Species Observed'


# Create a TabularInline to enter one or more Prevalent Behavior observed
class PrevalentBehaviorSightingInline(admin.TabularInline):
    model = Sighting.Behavior.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Prevalent Behavior'
    verbose_name_plural = 'Prevalent Behaviors'


# Create a TabularInline to enter one or more Research Activities
class ResearchActivitySightingInline(admin.TabularInline):
    model = Sighting.Activity.through
    extra = 0
    classes = ['collapse']
    verbose_name = 'Research Activity'
    verbose_name_plural = 'Research Activities'


# Create a TabularInline to enter one or more Images
class FileSightingInline(admin.TabularInline):
    model = File_Sighting
    extra = 0
    classes = ['collapse']
    verbose_name = 'Sighting File'
    verbose_name_plural = 'Sighting Files'


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
    list_filter = ('Date', 'First_Species_Observed')

    # Add a search field by 'Port','Date', 'First_Species_observed'
    search_fields = ('Port', 'Date',)

    # Insert a link on field
    list_display_links = ['Port']

    inlines = [DolphinSecondSpeciesSightingInline,
               PrevalentBehaviorSightingInline, ResearchActivitySightingInline,
               FileSightingInline]


# Register the model data for admin section
admin.site.register(Sighting, SightingAdmin)
admin.site.register(Prevalent_Behavior)
admin.site.register(Research_Activity)
admin.site.register(Dolphin_Species)
admin.site.register(Gallery)
admin.site.register(File_Sighting, FileSightingModelAdmin)
