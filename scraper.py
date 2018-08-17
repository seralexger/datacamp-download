# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/datacamp-download
#
#########################################################

import requests
import time
import random
import json
import re
import os

from lxml import html
from lxml import etree




class DataCamp:

	session = requests.Session()


	def __init__(self, user_email, user_pass):

		if not os.path.exists('courses'):
			os.makedirs('courses')

		if not os.path.exists('courses/courses_data'):
			os.makedirs('courses/courses_data')

		self.session.headers.update({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})
		r = self.session.get('https://www.datacamp.com/')
		tree = html.fromstring(r.content)
		authenticity_token = tree.xpath('//input[@name="authenticity_token"]/@value')[0]
		user_sign = self.sign_in(user_email, user_pass, authenticity_token)

	def sign_in(self, user_email, user_pass, authenticity_token):
		data = [
		  ('utf8', '\u2713'),
		  ('authenticity_token', authenticity_token),
		  ('how', 'inline_form_home_page'),
		  ('user[email]', user_email),
		  ('user[password]', user_pass),
		  ('commit', 'Sign in'),
		  ('user[remember_me]', '0'),
		]

		r = self.session.post('https://www.datacamp.com/users/sign_in', data=data)

		if r.status_code == 200:
			return True
		else:
			return False


	def exercise_data(self, chapter_url):

		r = self.session.get(chapter_url)

		return r.content

	def chapter_extractor(self, course_url):

		def add_data(exer, ex_data, index):

			exer['data'] = ex_data[index]

			return exer


		def exercise_class(exercise_li):

			if 'interactive' in exercise_li.xpath('.//img/@alt')[0]:
				exercise_dic = {}
				exercise_dic['url'] = exercise_li.xpath('.//a/@href')[0]
				#exercise_dic['url_data'] = 'https://campus-api.datacamp.com/api/courses/'+course_id+'/chapters/'+exercise_id+'/progress'
				exercise_dic['title'] = exercise_li.xpath('.//h5[@class="chapter__exercise-title"]/@title')[0]
				
				return exercise_dic

		if os.path.isfile('courses/courses_data/'+course_url.split('/')[-1]+'.json'):

			chapter_arr = json.loads(open('courses/courses_data/'+course_url.split('/')[-1]+'.json').read())['chapters']
		
		else:

			r = self.session.get(course_url)
			tree = html.fromstring(r.content)
			chapters = tree.xpath('//ol[@class="chapters"]/li[@class="chapter"]')
			course_id = re.search(r'tion/course_(.*?)/shields/', r.text).group(1)
			exercise_ids = tree.xpath('//span[@class="js-mobile-progress-container js-mobile-chapter-progress"]/@data-id')
			datasets_url = tree.xpath('//ul[@class="course__datasets"]/li/a/@href')
			datasets_name = [x.strip() for x in tree.xpath('//ul[@class="course__datasets"]/li/a/text()')]
			datasets = dict(zip(datasets_name, datasets_url))
			chapter_arr = []
			for index, chapter in enumerate(chapters):
				chapter_dic ={}
				chap_exe = self.session.get('https://campus-api.datacamp.com/api/courses/'+course_id+'/chapters/'+exercise_ids[index]+'/progress')
				cleaned_chap_exe = [x for x in chap_exe.json() if x['last_attempt'] == None or '#' in x['last_attempt']]
				chapter_dic['name'] = chapter.xpath('.//h4[@class="chapter__title"]/text()')[0].strip()
				chapter_dic['number'] = chapter.xpath('.//span[@class="chapter-number"]/text()')[0].strip()
				chapter_dic['description'] = chapter.xpath('.//p[@class="chapter__description"]/text()')[0].strip()
				chapter_dic['exercises'] = [exercise_class(x) for x in chapter.xpath('.//ul[@class="chapter__exercises hidden"]/li') if exercise_class(x) != None]
				chapter_dic['exercises'] = [add_data(x, cleaned_chap_exe, idx) for idx, x in enumerate(chapter_dic['exercises'])]
				chapter_arr.append(chapter_dic)
			with open('courses/courses_data/'+course_url.split('/')[-1]+'.json', 'w') as out:
				json.dump({'chapters':chapter_arr, 'datasets': datasets}, out, indent=4)

		return chapter_arr


	def create_source(self, course_url, chapter_number, chapter_name, exercise_number,exercise_name, data, sub=False):
		course_name = course_url.split('/')[-1]
		chapter_directory = 'courses/'+course_name+'/chapters/'+str(chapter_number)+'_'+chapter_name.replace('/', '_')
		if not os.path.exists('courses/'+course_name):
			os.makedirs('courses/'+course_name)
		if not os.path.exists(chapter_directory):
			os.makedirs(chapter_directory)
		if sub:
			aux = ''
			for index, item in enumerate(data):
				if 'selected_option' in item['last_attempt']:
					to_write = '#'+item['last_attempt']
				else:
					to_write = item['last_attempt']
				aux += '\n'+'\n'+'#'+exercise_name+' subexercise '+str(index)+'\n'+'\n'+ to_write
			data = aux
		with open(chapter_directory+'/'+str(exercise_number)+'_'+exercise_name.replace('/', '_')+'.py', 'w') as f:
			f.write(data)


	def download_course_source(self, course_url):
		data = self.chapter_extractor(course_url)
		for item in data:
			for idx, ex in enumerate(item['exercises']):
				if len(ex['data']['subexercises']) == 0:
					self.create_source(course_url, item['number'], item['name'], idx, ex['title'], ex['data']['last_attempt'], sub=False)
				else:
					self.create_source(course_url, item['number'], item['name'], idx, ex['title'], ex['data']['subexercises'], sub=True)



