# flickr-chronologise
A short python script to arrange your Flickr photostream chronologically. This script works by changing your upload date to match the date the photo was taken (found in the photos EXIF data).
You will need your API key, secret and your Flickr user id. More info can found at https://www.flickr.com/services/api/.

(Note: Photos will require accurate EXIF data. For photos taken prior to account creation, the script will arrange the photos and set their upload dates chronologically, with the respect to date/time of account creation, i.e. oldest photo upload date = account creation datetime + 1 second, second oldest photo upload date = account creation datetime + 2 seconds, ...)
