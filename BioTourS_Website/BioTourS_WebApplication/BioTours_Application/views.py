import haversine as gps_distance_library
from GPSPhoto import gpsphoto
from django.contrib.gis.geos import Point, MultiPoint
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from haversine import Unit
from .filters import SightingFilter
from .forms import SightingForm, FileSightingForm
from .models import Sighting, File_Sighting, Gallery


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

            ################################################
            #  For each file, check if there are exif_data,
            #  if these are valid, and if there are gps data
            ################################################
            list_gps_data_sightings = list()
            index_sightings_with_gps_data = list()
            index_sightings_without_gps_data = list()
            index_sighting_with_invalid_gps_data = list()

            for i in range(0, len(files_list)):
                try:
                    exif_data = gpsphoto.getGPSData(files_list[i].temporary_file_path())
                    latitude = exif_data.get('Latitude')
                    longitude = exif_data.get('Longitude')
                    if latitude is not None and longitude is not None:
                        if (-90 <= latitude <= 90) and (-180 <= longitude <= 180):
                            list_gps_data_sightings.append(Point(latitude, longitude))
                            index_sightings_with_gps_data.append(i)
                        else:
                            index_sighting_with_invalid_gps_data.append(i)
                    else:
                        index_sightings_without_gps_data.append(i)
                except IndexError:
                    index_sightings_without_gps_data.append(i)

            file_with_gps_data = [files_list[index_sightings_with_gps_data[i]]
                                  for i in range(0, len(index_sightings_with_gps_data))]

            file_without_gps_data = [files_list[index_sightings_without_gps_data[i]]
                                     for i in range(0, len(index_sightings_without_gps_data))]

            file_with_invalid_gps_data = [files_list[index_sighting_with_invalid_gps_data[i]]
                                          for i in range(0, len(index_sighting_with_invalid_gps_data))]

            #######################################################
            # Since we know now which files have valid and invalid
            # gps data and which files have no gps data, we focus
            # only on files with valid gps data.
            #######################################################

            list_nearest_sighting = list()
            list_rejected_sighting = list()

            # if we have at least 1 file with valid gps data, we can create a new sighting
            if file_with_gps_data:

                # Fetch sighting information
                port = form_sighting.cleaned_data.get('Port')
                date = form_sighting.cleaned_data.get('Date')
                notes = form_sighting.cleaned_data.get('Notes')

                num_files = len(file_with_gps_data)

                # If we have only one file, then we can use the gps data of it to create a new
                # data of it to create a new sighting
                if 0 < num_files <= 1:
                    list_nearest_sighting.append(file_with_gps_data[0])
                    new_sighting = Sighting.objects.create(Port=port, Date=date, Notes=notes,
                                                           Latitude_Contact=list_gps_data_sightings[0].x,
                                                           Longitude_Contact=list_gps_data_sightings[0].y)
                    File_Sighting.objects.create(file=list_nearest_sighting[0], sighting=new_sighting)

                else:
                    # In this case we have many files with gps data,
                    # so we have to check if the gps data of each file is in
                    # the radius we consider with respect to the centroid point
                    radius = 500
                    index_nearest_sighting = list()
                    set_of_index_files_sightings = set(i for i in range(0, num_files))
                    multipoint = MultiPoint(*list_gps_data_sightings)
                    center_point_sighting = multipoint.centroid

                    center_point = (center_point_sighting.x, center_point_sighting.y)

                    for i in range(0, num_files):
                        point2 = (list_gps_data_sightings[i].x, list_gps_data_sightings[i].y)
                        if gps_distance_library.haversine(center_point, point2, unit=Unit.METERS) <= radius:
                            index_nearest_sighting.append(i)

                    index_nearest_sighting = set(index_nearest_sighting)
                    index_rejected_sighting = list(set_of_index_files_sightings.difference(index_nearest_sighting))
                    index_nearest_sighting = list(index_nearest_sighting)

                    list_nearest_sighting = [file_with_gps_data[index_nearest_sighting[i]]
                                             for i in range(0, len(index_nearest_sighting))]

                    list_rejected_sighting = [file_with_gps_data[index_rejected_sighting[i]]
                                              for i in range(0, len(index_rejected_sighting))]

                    new_sighting = Sighting.objects.create(Port=port, Date=date, Notes=notes,
                                                           Latitude_Contact=center_point[0],
                                                           Longitude_Contact=center_point[1])
                    for i in range(0, len(list_nearest_sighting)):
                        File_Sighting.objects.create(file=list_nearest_sighting[i], sighting=new_sighting)

                submitted = True

            form_sighting = SightingForm()
            form_file_sighting = FileSightingForm()

            return render(request, 'BioToursApplication/insert_sighting_template.html',
                          {'submitted': submitted,
                           'list_file_without_gps_data': file_without_gps_data,
                           'list_file_with_invalid_gps_data': file_with_invalid_gps_data,
                           'list_nearest_sighting': list_nearest_sighting,
                           'list_rejected_sighting': list_rejected_sighting,
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

    paginated_filtered_sightings = Paginator(filtered_sightings.qs, 10)
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
    files_sighting = File_Sighting.objects.all().filter(sighting=sighting_detail)

    list_image_sighting = list()
    list_video_sighting = list()

    for file_sighting in files_sighting:
        if file_sighting.file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            list_image_sighting.append(file_sighting)
        else:
            list_video_sighting.append(file_sighting)

    template = 'BioToursApplication/sighting_details_template.html'
    context = {
        'sighting': sighting_detail,
        'image_files_sighting': list_image_sighting[0:12],
        'video_files_sighting': list_video_sighting[0:6],
    }
    return render(request, template, context)


def MapViewerView(request):
    filtered_sightings = SightingFilter(
        request.GET,
        queryset=Sighting.objects.get_queryset().order_by('pk')
    )
    template = 'BioToursApplication/map_viewer_template.html'
    context = {
        'filtered_sightings': filtered_sightings,
    }

    return render(request, template, context)


def GalleryView(request):
    gallery_files = Gallery.objects.all().order_by('-pk')
    list_image_gallery = list()
    list_video_gallery = list()

    for gallery_file in gallery_files:
        if gallery_file.file_gallery.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            list_image_gallery.append(gallery_file)
        else:
            list_video_gallery.append(gallery_file)

    template = 'BioToursApplication/gallery_template.html'
    context = {
        'image_files_gallery': list_image_gallery[0:21],
        'video_files_gallery': list_video_gallery[0:12],
    }
    return render(request, template, context)
