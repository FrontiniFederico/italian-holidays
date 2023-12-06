#!/bin/python
from datetime import datetime, timedelta
import sys
import os
import json
import math

with open('holidays.json') as file_json:
	standard_holidays: dict[str, str] = json.load(file_json)

print(standard_holidays["1-1"])


class ItalianHolidays():
	
	def __init__(self, custom_holidays: list = []):

		self._custom_holidays: list = custom_holidays

	def is_holiday(self, date: datetime) -> bool:
		"""Method tha determines whether a given day is a holiday

		:param date: the day the user is querying about
		:type date: datetime
		:return: the outcome
		:rtype: bool
		"""

		if not isinstance(date, str) and not isinstance(date, datetime):
			raise TypeError('is_holiday can accept only string or datetime object')
		date_obj: datetime = date
		if isinstance(date, str):
			try:
				date_obj: datetime = datetime.strptime(date, '%Y-%m-%d')
			except ValueError:
				raise ValueError('date must be in the format \'Y-m-d\'')
		# we first check whether the date object is a standard holyday
		# as in those holydays that always happen the same day
		date_str: str = f"{date_obj.month}-{date_obj.day}"
		if date_str in standard_holidays:
			return True
		# we now check if it's Easter
		if date_obj.month == self._easter(date_obj).month and date_obj.day == self._easter(date_obj).day:
			return True
		if date_obj.month == self._easter_monday(date_obj).month and date_obj.day == self._easter_monday(date_obj).day:
			return True
		if self._custom_holidays:
			for custom_holiday in self._custom_holidays:
				if not isinstance(custom_holiday, str) and not isinstance(custom_holiday, datetime):
					raise TypeError('custom holidays can accept only list of strings or datetime objects')
				custom_date_obj = custom_holiday
				if isinstance(custom_holiday, str):
					custom_date_obj = datetime.strptime(custom_holiday, '%m-%d')
				if date_obj.month == custom_date_obj.month and date_obj.day == custom_date_obj.day:
					return True
		return False

	def holiday_name(self, date):
		if isinstance(date, str) == False and isinstance(date, datetime) == False:
			return sys.exit('holiday_name can accept only string or datetime object')
		date_obj = date
		if isinstance(date, str):
			date_obj = datetime.strptime(date, '%Y-%m-%d')
		if date_obj is None:
			return sys.exit('date must be in the format \'Y-m-d\'')
		name = None
		if date_obj.month == 1 and date_obj.day == 1:
			name = 'New Year\'s Day'
		if date_obj.month == 1 and date_obj.day == 6:
			name = 'Epiphany'
		if date_obj.month == self._easter(date_obj).month and date_obj.day == self._easter(date_obj).day:
			name = 'Easter Sunday'
		if date_obj.month == self._easter_monday(date_obj).month and date_obj.day == self._easter_monday(date_obj).day:
			name = 'Easter Monday'
		if date_obj.month == 4 and date_obj.day == 25:
			name = 'Liberation Day'
		if date_obj.month == 5 and date_obj.day == 1:
			name = 'Labor Day / May Day'
		if date_obj.month == 6 and date_obj.day == 2:
			name = 'Republic Day'
		if date_obj.month == 8 and date_obj.day == 15:
			name = 'Ferragosto'
		if date_obj.month == 11 and date_obj.day == 1:
			name = 'All Saints\' Day'
		if date_obj.month == 12 and date_obj.day == 8:
			name = 'Solemnity of the Immaculate Conception'
		if date_obj.month == 12 and date_obj.day == 25:
			name = 'Christmas Day'
		if date_obj.month == 12 and date_obj.day == 26:
			name = 'St. Stephen\'s Day'
		if self._custom_holidays:
			for custom_holiday in self._custom_holidays:
				if not isinstance(custom_holiday, str) and not isinstance(custom_holiday, datetime):
					raise TypeError('custom holidays can accept only array of string or datetime object')
				custom_date_obj = custom_holiday
				if isinstance(custom_holiday, str):
					custom_date_obj = datetime.strptime(custom_holiday, '%m-%d')
				if date_obj.month == custom_date_obj.month and date_obj.day == custom_date_obj.day:
					return 'Custom holiday'
		return name

	def _easter(self, year: str) -> str:
		"""Implementation of the Gauss algorithm to find Easter

		:param year: the year to check
		:type year: str
		:return: Easter Sunday
		:rtype: str
		"""
		easter: str = ""
		# Only God and Gauss know how he came up with this stuff
		A = year % 19
		B = year % 4
		C = year % 7
		P = math.floor(year / 100)
		Q = math.floor((13 + 8 * P) / 25)
		M = (15 - Q + P - P // 4) % 30
		N = (4 + P - P // 4) % 7
		D = (19 * A + M) % 30
		E = (2 * B + 4 * C + 6 * D + N) % 7
		days: int = (22 + D + E)
		# A corner case,
		# when D is 29
		if ((D == 29) and (E == 6)):
			easter = year + "-04-19"
		# Another corner case,
		# when D is 28
		elif ((D == 28) and (E == 6)):
			easter = year + "-04-18"
		else:
			# If days > 31, move to April
			# April = 4th Month
			if (days > 31):
				easter = year + "-04-" + (days - 31)
			else:
				# Otherwise, stay on March
				# March = 3rd Month
				easter = year +"-03-" + days
		return easter

	def _easter_monday(self, date):
		return self._easter(date) + timedelta(1)