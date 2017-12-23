import requests
import re
from io import BytesIO

class Parser:
	memberId = 1000
	
	def __init__(self, startMemberId):
		self.memberId = startMemberId
	
	def request(self):
		url = 'http://www.sql.ru/forum/memberinfo.aspx?mid=' + str(self.memberId)
		self.content = requests.get(url).text
		return self

	def requestEmailImg(self):
		if not hasattr(self, 'emailImgUrl'):
			raise ValueError('Member have hidden email')
		else:
			url = 'http://www.sql.ru/forum/' + self.emailImgUrl
		return BytesIO(requests.get(url).content)
	
	def parsePage(self):
		match = re.search('src="(afemailimage\.aspx\?data=[\w\W]+?)"', self.content)
		if match:
			self.emailImgUrl = match.group(1)
		return self
		
