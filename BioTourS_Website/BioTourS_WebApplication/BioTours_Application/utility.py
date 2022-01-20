from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
from scipy.spatial import distance
import haversine as gps_distance_library


def get_lat_long(image_file):
    image = Image.open(image_file)

    exif = {}

    for tag, value in image.getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'GPSInfo' in exif:
        geo_coordinate = '{0} {1} {2:.2f} {3}, {4} {5} {6:.2f} {7}'.format(
            exif['GPSInfo'][2][0][0],
            exif['GPSInfo'][2][1][0],
            exif['GPSInfo'][2][2][0] / exif['GPSInfo'][2][2][1],
            exif['GPSInfo'][1],
            exif['GPSInfo'][4][0][0],
            exif['GPSInfo'][4][1][0],
            exif['GPSInfo'][4][2][0] / exif['GPSInfo'][4][2][1],
            exif['GPSInfo'][3]
        )

    # list_exif = ', '.join([str(value) for tag, value in image.getexif().items()])

    return geo_coordinate


def find_near_sighting():
    """
    list_files = list()
    list_files.append('img1')
    list_files.append('img2')
    list_files.append('img3')
    list_files.append('img4')

    set_of_index_files_sightings = list(np.linspace(0, len(list_files) - 1, len(list_files)))

    for i in range(0, len(set_of_index_files_sightings)):
        set_of_index_files_sightings[i] = int(set_of_index_files_sightings[i])

    set_of_index_files_sightings = set(set_of_index_files_sightings)

    image_gps_location_1 = (11.2, 35.6)
    image_gps_location_2 = (40.52, 90.6)
    image_gps_location_3 = (12.26, 36.6)
    image_gps_location_4 = (35.2, 50.2)

    list_of_gps_location_sighting = list()

    list_of_gps_location_sighting.append(image_gps_location_1)
    list_of_gps_location_sighting.append(image_gps_location_2)
    list_of_gps_location_sighting.append(image_gps_location_3)
    list_of_gps_location_sighting.append(image_gps_location_4)

    num_el = len(list_of_gps_location_sighting)

    distance_matrix = np.zeros([num_el, num_el])

    for i in range(0, num_el - 1):
        for j in range(i + 1, num_el):
            distance_matrix[i][j] = gps_distance_library.haversine(list_of_gps_location_sighting[i],
                                                                   list_of_gps_location_sighting[j])

    list_of_image_coupled = list()

    for i in range(0, num_el - 1):
        for j in range(i + 1, num_el):
            if distance_matrix[i][j] < 30:
                list_of_image_coupled.append((i, j))

    subset_of_same_sighting = set()

    for i in range(0, len(list_of_image_coupled)):
        subset_of_same_sighting.add(list_of_image_coupled[i][0])
        subset_of_same_sighting.add(list_of_image_coupled[i][1])

    sublist_of_same_sighting = list(subset_of_same_sighting)
    sublist_of_different_sighting = list(set_of_index_files_sightings.difference(sublist_of_same_sighting))

    return sublist_of_same_sighting, sublist_of_different_sighting

    return distance_matrix.tolist()
"""