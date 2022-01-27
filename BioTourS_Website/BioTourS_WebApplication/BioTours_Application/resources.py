# Define a resource to be used for db export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, DateWidget, TimeWidget
from BioTours_Application.models import Dolphin_Species, Prevalent_Behavior, Research_Activity, Sighting


class SightingResource(resources.ModelResource):
    Port = fields.Field(attribute='Port', column_name='Port')
    Date = fields.Field(attribute='Date', column_name='Date', widget=DateWidget())
    Start_Activity_Time = fields.Field(attribute='Start_Activity_Time', column_name='Start_Activity_Time',
                                       widget=TimeWidget())
    End_Activity_Time = fields.Field(attribute='End_Activity_Time', column_name='End_Activity_Time',
                                     widget=TimeWidget())
    Start_Contact_Time = fields.Field(attribute='Start_Contact_Time', column_name='Start_Contact_Time',
                                      widget=TimeWidget())
    End_Contact_Time = fields.Field(attribute='End_Contact_Time', column_name='End_Contact_Time',
                                    widget=TimeWidget())
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

        export_order = ['id', 'Port', 'Latitude_Contact', 'Longitude_Contact', 'Date', 'Start_Activity_Time',
                        'End_Activity_Time', 'Start_Contact_Time', 'End_Contact_Time', 'First_Species_Observed',
                        'Number_Individuals', 'Number_Calves', 'Depth', 'Second_Species_Observed', 'Behavior',
                        'Activity', 'Other_Boats', 'Fishing_Gear_Available', 'Interaction_With_Gear', 'Other_Organism',
                        'Notes']

        exclude = ['Gps_Location']

