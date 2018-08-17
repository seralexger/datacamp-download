# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/datacamp-download
#
#########################################################

from scraper import DataCamp
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-u","--user", help="DataCamp user")
ap.add_argument("-p","--pass", help="DataCamp pass")
ap.add_argument("-q","--query", help="Course url")
args = vars(ap.parse_args())


scraper = DataCamp(args['user'],  args['pass'])
scraper.download_course_source(args['query'])
print('Done')