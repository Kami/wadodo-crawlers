import json

import flickrapi

__all__ = [
    'get_images_for_term'
]

PER_PAGE = 40
# http://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html
LICENSES = [4, 5, 6, 7]
CONTENT_TYPES = [1]
SORT = 'relevance'
BASE_URL = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(id)s_%(secret)s_b.jpg'

FLICKR_CLIENT = None


def parse_result(result):
    # Wow, this library sucks.
    result = result.replace('jsonFlickrApi(', '')[:-1]
    result = json.loads(result)
    return result


def get_images_for_term(api_key, search_term, bbox=None, count=5):
    global FLICKR_CLIENT

    if not FLICKR_CLIENT:
        FLICKR_CLIENT = flickrapi.FlickrAPI(api_key, cache=False)

    flickr = FLICKR_CLIENT
    result = flickr.photos_search(text=search_term, per_page=PER_PAGE,
                                  license=LICENSES, content_type=CONTENT_TYPES,
                                  sort=SORT, bbox=bbox, format='json')
    result = parse_result(result)
    photos = result['photos']['photo']

    result = []
    for photo in photos:
        info = flickr.photos_getInfo(photo_id=photo['id'], format='json')
        info = parse_result(info)['photo']
        sizes = flickr.photos_getSizes(photo_id=photo['id'], format='json')
        sizes = parse_result(sizes)['sizes']['size']
        sizes = [(int(size['width']), int(size['height'])) for size in sizes]
        max_size = max(sizes)

        if max_size[0] < 1024:
            continue

        owner = info['owner']
        photo_url = BASE_URL % ({'farm_id': photo['farm'], 'server_id': photo['server'],
                                 'id': photo['id'], 'secret': photo['secret']})

        item = {'url': photo_url, 'owner': owner}
        result.append(item)

        if len(result) >= count:
            break

    return result
