#!/bin/python
from datetime import datetime, timedelta
import sys
from dotenv import load_dotenv
import os
import json

load_dotenv()
holiday_list = json.loads(os.getenv('STANDARD_HOLYDAYS', " "))


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
		if date_str in holiday_list:
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

	def _easter(self, date: datetime):
		''' 
		***********************
		WORKS FROM 1900 TO 2199
		***********************
		'''
		gold_numbers = {0: 19, 1: 45, 2: 34, 3: 23, 4: 42, 5: 31, 6: 49, 7: 39, 8: 28, 9: 47, 10: 36, 11: 25, 12: 44, 13: 33, 14: 22, 15: 41, 16: 30, 17: 48, 18: 38, 19: 27}
		cycle_19_year = 1918
		year = int(date.strftime('%Y'))
		modulo = (year + 1) % 19
		gold_number = gold_numbers[modulo]
		if gold_number <= 31:
			full_moon = datetime(year, 3, gold_number)
			easter_date = None
			if full_moon.weekday() == 6:
				easter_date = full_moon + timedelta(days= 7)
			else:
				easter_date = full_moon
				while easter_date.weekday() != 6:
					easter_date = easter_date + timedelta(days= 1)
			if (easter_date.year - cycle_19_year) % 19 == 0:
				easter_date = easter_date + timedelta(days=7)
			return easter_date
		else:
			day = gold_number - 31
			full_moon = datetime(year, 4, day)
			easter_date = None
			if full_moon.weekday() == 6:
				easter_date = full_moon + timedelta(days= 7)
			else:
				easter_date = full_moon
				while easter_date.weekday() != 6:
					easter_date = easter_date + timedelta(days= 1)
			return easter_date

	def _easter_monday(self, date):
		return self._easter(date) + timedelta(1)