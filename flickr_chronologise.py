from datetime import timedelta
from datetime import datetime
import json
import time

import webbrowser
import flickrapi

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

flickr_key = '[YOUR_API_KEY]'
flickr_secret = '[YOUR_API_SECRET]'

flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='json')

joined_flickr = datetime.fromtimestamp(int(json.loads(flickr.people.getInfo(user_id='[YOUR_FLICKR_USER_ID]').decode("utf-8"))['person']['photos']['firstdate']['_content']))

all_photos = []

print('-----> Fetching all photos')

res = (flickr.photos_search(user_id='[YOUR_FLICKR_USER_ID]', extras='date_upload,date_taken', per_page='490', page='1').decode('utf_8'))

pics = json.loads(res.replace("jsonFlickrApi(", "").replace(")", ""))

photos = pics['photos']['photo']

all_photos.extend(photos)

if joined_flickr is not None:
    def datetaken(photo):
        return datetime.strptime(photo['datetaken'], DATE_FORMAT)
    photos_before_joined = []
    photos_after_joined = []
    for p in all_photos:
        if datetaken(p) <= joined_flickr:
            photos_before_joined.append(p)
        else:
            photos_after_joined.append(p)
    photos_before_joined = sorted(photos_before_joined, key=datetaken)
    for i, p in enumerate(photos_before_joined):
        p['datetaken'] = (joined_flickr + timedelta(0,i)).strftime(DATE_FORMAT)
    all_photos = photos_before_joined + photos_after_joined
    
print('-----> Now authenticate')

if not flickr.token_valid(perms='write'):
    flickr.get_request_token(oauth_callback='oob')
    authorize_url = flickr.auth_url(perms='write')
    webbrowser.open_new_tab(authorize_url)
    verifier = str(input('-----> Verifier code: '))
    flickr.get_access_token(verifier)


print('-----> Updating dates')

for photo in  all_photos:
    date_taken = photo['datetaken']
    date_taken = datetime.strptime(date_taken, DATE_FORMAT)
    date_posted = int(photo['dateupload'])
    date_posted = datetime.fromtimestamp(date_posted)
    if date_posted != date_taken:
        print('       Updating "{}": change date posted from {} to {}'.format(photo['id'], date_posted, date_taken))
        new_date_posted = datetime.strftime(date_taken, '%s')
        flickr.photos_setDates(photo_id=photo['id'], date_posted=new_date_posted)
        new_date_posted = time.mktime(date_taken.timetuple())
        res = flickr.photos_setDates(photo_id=photo['id'], date_posted=new_date_posted)
    else:
        print('       Skipping "{}": dates match'.format(photo['id']))
print('-----> Done!')



