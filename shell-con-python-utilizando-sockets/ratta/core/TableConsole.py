"""
	This class is not mine. I don't know the creator
"""
from termcolor import cprint

class Table:
	margin_left = 3
	margin_right = 3
	
	columns_str = '|'
	rows_str = ''
	columns_size = []

	def reset(self):
		self.margin_left = 3
		self.margin_right = 3

		self.columns_str = '|'
		self.rows_str = ''
		self.columns_size = []

	def formatText(self, text, width):
		content = text
		
		for i in range(0, width-len(content)):
			content += " "
		return content
		
	def addColumn(self, title, width):
		self.columns_str += self.formatText("", self.margin_left) + self.formatText(title, width) + self.formatText("", self.margin_right) + "|"
		self.columns_size.append(width)

	def addRow(self, data):
		col = 0
		row = '|'
		for d in data: 
			row += self.formatText("", self.margin_left) + self.formatText(d, self.columns_size[col]) + self.formatText("", self.margin_right) + "|"
			col= col+1
		self.rows_str += row + "\r\n"
		
	def make(self, title, color):
		max_chars = 0
		for i in list(self.columns_size):
			max_chars += i
			
		max_chars += (self.margin_left*len(self.columns_size)) + (self.margin_right*len(self.columns_size))
		
		max_chars += len(self.columns_size)+1
		lineTitle = "+-" + title.title()
		for i in range(max_chars-(len(title)+2)):
			lineTitle += "-"
		separator_str = ''
		for i in range(max_chars):
			separator_str += "-"

		cprint("\n" + lineTitle, color)
		cprint(self.columns_str, color)
		cprint(separator_str, color)
		cprint(self.rows_str.strip(), color)
		cprint(separator_str + "\n", color)