# encoding: utf-8

class Message(object):
	"""docstring for Message"""
	def __init__(self, type = 'undefined'):
		super(Message, self).__init__()
		self.arg = arg
		self.type = type
		self.size = 8
		self.id = '1234' + 'time'
		self.ack_number = -1
		self.content = []

	def add_content(self, content):
		self.content.append(content)

	def get_id(self):
		return self.id

	def set_ack_number(self, ack_number):
		self.ack_number = ack_number

	def get_ack_number(self):
		return self ack_number