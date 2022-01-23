# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.gis.db.models import PointField
from django.contrib.gis.forms import OSMWidget
from django.db.models import DateField, TimeField
from import_export.admin import ExportMixin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from .models import Prevalent_Behavior, Research_Activity, Dolphin_Species, Sighting, File_Sighting, Gallery
from .forms import DateInput, TimeInput

# Removed 'Group' from admin section
admin.site.unregister(Group)

# Change header name in the administration section
admin.site.site_header = 'BioTourS Admin Dashboard'

# Change title name of site
admin.site.site_title = 'BioTourS Admin Dashboard'

admin.site.index_title = ''

# Corresponding to the tab 'View Site'
admin.site.site_url = ''


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'approval', 'company_view',)
    list_filter = ('approval',)


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


# Define a resource to be used for db export
class SightingResource(resources.ModelResource):
    Port = fields.Field(attribute='Port', column_name='Port')
    Date = fields.Field(attribute='Date', column_name='Date')
    Start_Activity_Time = fields.Field(attribute='Start_Activity_Time', column_name='Start_Activity_Time')
    End_Activity_Time = fields.Field(attribute='End_Activity_Time', column_name='End_Activity_Time')
    Start_Contact_Time = fields.Field(attribute='Start_Contact_Time', column_name='Start_Contact_Time')
    End_Contact_Time = fields.Field(attribute='End_Contact_Time', column_name='End_Contact_Time')
    Latitude_Contact = fields.Field(attribute='Latitude_Contact', column_name='Latitude_Contact')
    Longitude_Contact = fields.Field(attribute='Longitude_Contact', column_name='Longitude_Contact')
    Depth = fields.Field(attribute='Depth', column_name='Depth')
    First_Species_Observed = fields.Field(attribute='First_Species_Observed', column_name='First_Species_Observed',
                                          widget=ForeignKeyWidget(model=Dolphin_Species, field='Name_Species'))
    Second_Species_Observed = fields.Field(attribute='Second_Species_Observed', column_name='Second_Species_Observed',
                                           widget=ManyToManyWidget(model=Dolphin_Species, separator=';',
                                                                   field='Name_Species'))
    Number_Individuals = fields.Field(attribute='Number_Individuals', column_name='Number_Individuals')
    Number_Calves = fields.Field(attribute='Number_Calves', column_name='Number_Calves')
    Behavior = fields.Field(attribute='Behavior', column_name='Prevalent_Behavior',
                            widget=ManyToManyWidget(model=Prevalent_Behavior, separator=';', field='Behavior'))
    Activity = fields.Field(attribute='Activity', column_name='Research_Activity',
                            widget=ManyToManyWidget(model=Research_Activity, separator=';', field='Activity'))
    Other_Boats = fields.Field(attribute='Other_Boats', column_name='Other_Boats')
    Fishing_Gear_Available = fields.Field(attribute='Fishing_Gear_Available', column_name='Fishing_Gear_Available')
    Interaction_With_Gear = fields.Field(attribute='Interaction_With_Gear', column_name='Interaction_With_Gear')
    Other_Organism = fields.Field(attribute='Other_Organism', column_name='Other_Organism')
    Notes = fields.Field(attribute='Notes', column_name='Notes')

    class Meta:
        model = Sighting


# Define a layout for Sighting field, grouping in different fieldset
class SightingAdmin(ExportMixin, admin.ModelAdmin):
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
