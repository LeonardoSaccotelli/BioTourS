from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from haversine import Unit
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from .filters import SightingFilter

from .forms import SightingForm, FileSightingForm
from .models import Sighting, File_Sighting
import numpy as np
from GPSPhoto import gpsphoto
import haversine as gps_distance_library

"""
The HomepageView() method is the view that handles
the request to the homepage.
"""


def HomepageView(request):
    return render(request, 'BioToursApplication/index_template.html')


def AboutView(request):
    return render(request, 'BioToursApplication/about_template.html')


def InsertSightingView(request):
    submitted = False

    if request.method == 'POST':
        form_sighting = SightingForm(request.POST)
        form_file_sighting = FileSightingForm(request.POST, request.FILES)

        if form_sighting.is_valid() and form_file_sighting.is_valid():
            files_list = request.FILES.getlist('file')
            num_files = len(files_list)

            set_of_index_files_sightings = set()
            for index_file in range(0, len(files_list)):
                set_of_index_files_sightings.add(index_file)

            ################################################
            #  Per ogni files, recupero latitudine e longitudine
            ################################################
            exif_data_sightings = list()

            """if 0 < num_files < 2:
                exif_data_sightings.append(gpsphoto.getGPSData(files_list[0].))
            elif num_files >= 2:"""
            for image_file in files_list:
                path = image_file.temporary_file_path()
                exif_data_sightings.append(gpsphoto.getGPSData(path))

            """
            exif_data_sightings = list()
            exif_data_sightings.append((12.2, 35.6))
            exif_data_sightings.append((12.21, 35.6))
            exif_data_sightings.append((21.2, 35.61))
            exif_data_sightings.append((31.21, 35.62))
        
            exif_data_sightings.append((11.21, 35.6))
            exif_data_sightings.append((11.21, 35.61))
            exif_data_sightings.append((11.2, 35.61))
            exif_data_sightings.append((11.21, 35.62))
            """

            """
            num_files = len(exif_data_sightings)
            distance_matrix = np.zeros([num_files, num_files])
            radius = 1500

            list_of_distance_point_coupled = list()
            for i in range(0, num_files - 1):
                for j in range(i + 1, num_files):
                    point1 = (exif_data_sightings[i]['Latitude'], exif_data_sightings[i]['Longitude'])
                    point2 = (exif_data_sightings[j]['Latitude'], exif_data_sightings[j]['Longitude'])

                    distance_matrix[i][j] = gps_distance_library.haversine(point1, point2, unit=Unit.METERS)
                    if distance_matrix[i][j] < radius :
                        list_of_distance_point_coupled.append((i, j))

            subset_of_same_sighting = set()

            for i in range(0, len(list_of_distance_point_coupled)):
                subset_of_same_sighting.add(list_of_distance_point_coupled[i][0])
                subset_of_same_sighting.add(list_of_distance_point_coupled[i][1])

            different_sighting = list(set_of_index_files_sightings.difference(subset_of_same_sighting))
            same_sighting = list(subset_of_same_sighting)

            accepted_files = False
            accepted_files_name = list()
            if len(same_sighting) > 0:
                accepted_files = True

                port = form_sighting.cleaned_data.get('Port')
                date = form_sighting.cleaned_data.get('Date')
                notes = form_sighting.cleaned_data.get('Notes')

                new_sighting = Sighting.objects.create(Port=port, Date=date, Notes=notes)

                for i in range(0, len(same_sighting)):
                    accepted_files_name.append(files_list[same_sighting[i]])
                    File_Sighting.objects.create(file=files_list[same_sighting[i]], sighting=new_sighting)

            rejected_files = False
            rejected_files_name = list()
            if len(different_sighting) > 0:
                rejected_files = True
                for i in range(0, len(different_sighting)):
                    rejected_files_name.append(files_list[different_sighting[i]])
            """
            form_sighting = SightingForm()
            form_file_sighting = FileSightingForm()
            submitted = True

            return render(request, 'BioToursApplication/insert_sighting_template.html',
                          {'submitted': submitted,
                           'list2': exif_data_sightings,
                           # 'same_sighting': same_sighting,
                           # 'different_sighting': different_sighting,

                           # 'accepted_files': accepted_files,
                           # 'accepted_files_name': accepted_files_name,

                           # 'rejected_files': rejected_files,
                           # 'rejected_files_name': rejected_files_name,
                           # 'distance_matrix': distance_matrix,
                           'form_sighting': form_sighting,
                           'form_file_sighting': form_file_sighting,
                           })

    else:
        form_sighting = SightingForm()
        form_file_sighting = FileSightingForm()

    return render(request,
                  'BioToursApplication/insert_sighting_template.html',
                  {'form_sighting': form_sighting,
                   'form_file_sighting': form_file_sighting,
                   'submitted': submitted, })


def ShowSightingView(request):
    num_rows = Sighting.objects.all().count()
    filtered_sightings = SightingFilter(
        request.GET,
        queryset=Sighting.objects.get_queryset().order_by('pk')
    )

    paginated_filtered_sightings = Paginator(filtered_sightings.qs, 3)
    page_number = request.GET.get('page', 1)
    sighting_page_obj = paginated_filtered_sightings.get_page(page_number)

    try:
        items = paginated_filtered_sightings.page(page_number)
    except PageNotAnInteger:
        items = paginated_filtered_sightings.page(1)
    except EmptyPage:
        items = paginated_filtered_sightings.page(paginated_filtered_sightings.num_pages)

    index = items.number - 1
    max_index = len(paginated_filtered_sightings.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginated_filtered_sightings.page_range[start_index: end_index]

    template = 'BioToursApplication/show_sighting_template.html'
    context = {
        'num_rows': num_rows,
        'filtered_sightings': filtered_sightings,
        'sighting_page_obj': sighting_page_obj,
        'page_range': page_range,
    }

    return render(request, template, context)


def DetailSightingView(request, sighting_pk):
    sighting_detail = Sighting.objects.get(pk=sighting_pk)
    files_sighting = File_Sighting.objects.all().filter(sighting=sighting_detail)[0:2]

    template = 'BioToursApplication/sighting_details_template.html'
    context = {
        'sighting': sighting_detail,
        'files_sighting': files_sighting
    }
    return render(request, template, context)


def MapViewerView(request):
    return render(request, 'BioToursApplication/map_viewer_template.html')


def GalleryView(request):
    return render(request, 'BioToursApplication/gallery_template.html')
