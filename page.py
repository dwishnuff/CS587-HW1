class page:
	# a page basically contains a pageNo and content.
	# the content typically contains a few records. However, we use a string for simplicity
	def __init__(self, pageNo=None, content=None):
		if pageNo is None:
			self.pageNo = -1
		else:
			self.pageNo = pageNo

		if content is None:
			self.content = ""
		else:
			self.content = content
