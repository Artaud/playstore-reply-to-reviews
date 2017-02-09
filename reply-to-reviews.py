#!/usr/bin/python2
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Urbandroid Team reply to REVIEWS from PLAY STORE."""
# The api is https://developers.google.com/android-publisher/api-ref/reviews
# Quotas https://developers.google.com/android-publisher/reply-to-reviews
# How to run as cron: http://unix.stackexchange.com/questions/56491/interactive-shell-with-environment-identical-to-cron

import argparse
import sys
from apiclient import sample_tools
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('package_name',
                       help='The package name. Example: com.android.sample')


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv,
      'androidpublisher',
      'v2',
      __doc__,
      __file__,
      parents=[argparser],
      scope='https://www.googleapis.com/auth/androidpublisher')

  # Process flags and read their values.
  package_name = flags.package_name
  # review_id = "gp:AOqpTOEsF2l9Ecz5YKMnZyTW7I0gBlMEUbUaf5P3jucML9gy9OPXVTTwz0jp6UlVAQP61XWPoe2ssVMsM2Wt9Q"

  nextToken = ''


  try:
    # reviews_request = service.reviews().get(packageName=package_name, reviewId=review_id)


    if nextToken == '':
      reviews_request = service.reviews().list(packageName=package_name, translationLanguage='en', maxResults=50)
    else:
      reviews_request = service.reviews().list(packageName=package_name, translationLanguage='en', maxResults=50, token=nextToken)

    reviews_result = reviews_request.execute()
    # print reviews_result
    # print reviews_result['tokenPagination']['nextPageToken']
    # nextToken = reviews_result['tokenPagination']['nextPageToken']

    print "============================================="

    # print reviews_result['tokenPagination']
    reviews = reviews_result['reviews']

    for review in reviews:
      review_id = review['reviewId']

      # if 'authorName' in review:
        # print review['authorName']

      # print review_id
      # print review

      usercomment = review['comments'][0]['userComment']
      print usercomment['text'].encode('utf-8')
      if 'originalText' in usercomment:
        print usercomment['originalText'].encode('utf-8')
      print usercomment['reviewerLanguage']
      rating = usercomment['starRating']
      print rating

      if len(review['comments']) > 1:
        # Has dev comment - we've already replied
        devcomment = review['comments'][1]['developerComment']
        print devcomment['text'].encode('utf-8')
      else:
        # No dev comment
        if rating < 5:
          replyToReview(service, package_name, review_id)

      print "----------------------------------------------------"

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

def replyToReview(service, package_name, review_id):
  universalCannedResponse = "Many thanks for your valuable feedback. We are unfortunately unable to react to all of the reviews on Google Play Store. To resolve any issues with the app, it is best to contact us on our support email: support@urbandroid.org or to give us more details, use menu-report a bug. Many thanks. Jiri from Urbandroid Team."
  reply_request = service.reviews().reply(body={"replyText": universalCannedResponse}, packageName=package_name, reviewId=review_id)
  reply_request.execute()
  print 'Replied to review'


if __name__ == '__main__':
  main(sys.argv)

  # sample = {
  #   "authorName": "Joe Bergmann",
  #   "reviewId": "gp:AOqpTOFpm0yFEXsL_xjTrGQo7Rd7LgXCxl2k59hsQO3EBEo-spCsCzc3ivYVVjr4Acg7-MjZzASyprnVCWRg1g",
  #   "comments": [
  #     {
  #       "userComment":
  #       {
  #         "appVersionCode": 1440,
  #         "reviewerLanguage": "en_US",
  #         "text": "WHAT KIND OF ALARM TIMES OUT WHEN YOU DON'T TOUCH IT. A good alarm should endlessly go off until I turn it off. Terrible to have that as a default setting",
  #         "thumbsUpCount": 0,
  #         "starRating": 3,
  #         "lastModified":
  #         {
  #           "seconds":
  #           "1486482936",
  #           "nanos": 525000000
  #         },
  #         "device": "heroqltevzw",
  #         "androidOsVersion": 23,
  #         "deviceMetadata":
  #         {
  #           "screenDensityDpi": 640,
  #           "screenHeightPx": 2560,
  #           "cpuModel":
  #           "MSM8996",
  #           "glEsVersion": 196609,
  #           "productName": "heroqltevzw (Galaxy S7)",
  #           "nativePlatform": "armeabi-v7a,armeabi,arm64-v8a",
  #           "screenWidthPx": 1440,
  #           "cpuMake": "Qualcomm",
  #           "ramMb": 4096,
  #           "deviceClass": "phone",
  #           "manufacturer": "Samsung"
  #         },
  #         "appVersionName": "20161122",
  #         "thumbsDownCount": 0
  #       }
  #     },
  #     {
  #       "developerComment":
  #       {
  #         "text":
  #         "The delay for the alarm to time out is 20 min even then it only snoozed to restart the alarm later on for another 20 minutes.The reason for this are real cases reported by users where they forgot their phone in a locker for example..Many thanks for your feedback. You can change the alarm time out up to 2 hours..usually 20min is fine of everyone ;)",
  #         "lastModified":
  #         {
  #           "seconds":
  #           "1486486580",
  #           "nanos": 628000000
  #         }
  #       }
  #     }
  #   ]
  # }



