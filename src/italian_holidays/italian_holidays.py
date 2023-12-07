from datetime import datetime, timedelta
import sys
import os
import json
import math

with open('holidays.json') as file_json:
	holidays_dict: dict[str, str] = json.load(file_json)


class ItalianHolidays():
	
	def __init__(self, custom_holidays: list = []):

		self._custom_holidays: list[str | datetime] = custom_holidays

	def is_holiday(self, date: datetime) -> bool:
		"""Method tha determines whether a given day is a holiday

		:param date: the day the user is querying about
		:type date: datetime
		:return: the outcome
		:rtype: bool
		"""
		# from the year in the date passed to the caller 
		# we add easter related holidays to the dict
		if not isinstance(date, str) and not isinstance(date, datetime):
			raise TypeError('is_holiday can accept only string or datetime object')
		date_obj: datetime | str = date
		if isinstance(date, str):
			try:
				date_obj = datetime.strptime(date, '%Y-%m-%d')
			except ValueError:
				raise ValueError('date must be in the format \'Y-m-d\'')
		self._add_easter_holidays(year=int(date_obj.year))
		# we then check whether the date is in there
		date_str: str = f"{date_obj.month}-{date_obj.day}"
		if date_str in holidays_dict:
			return True
		for custom_holiday in self._custom_holidays:
			if not isinstance(custom_holiday, str) and not isinstance(custom_holiday, datetime):
				raise TypeError('custom holidays can accept only list of strings or datetime objects')
			custom_date_obj: datetime | str = custom_holiday
			if isinstance(custom_holiday, str):
				custom_date_obj = datetime.strptime(custom_holiday, '%m-%d')
			if date_obj.month == custom_date_obj.month and date_obj.day == custom_date_obj.day:
				return True
		return False

	def holiday_name(self, date):
		if not isinstance(date, str) and not (date, datetime):
			raise TypeError('is_holiday can accept only string or datetime object')
		date_obj: datetime | str = date
		try:
				date_obj = datetime.strptime(date, '%Y-%m-%d')
		except ValueError:
				raise ValueError('date must be in the format \'Y-m-d\'')
		date_str: str = f"{date_obj.month}-{date_obj.day}"
		name: str = None
		if date_str in holidays_dict:
			name = holidays_dict[date_str]
		if self._custom_holidays:
			for custom_holiday in self._custom_holidays:
				if not isinstance(custom_holiday, str) and not isinstance(custom_holiday, datetime):
					raise TypeError('custom holidays can accept only array of string or datetime object')
				custom_date_obj: datetime | str = custom_holiday
				if isinstance(custom_holiday, str):
					custom_date_obj = datetime.strptime(custom_holiday, '%m-%d')
				if date_obj.month == custom_date_obj.month and date_obj.day == custom_date_obj.day:
					return 'Custom holiday'
		return name

	def _easter(self, year: int) -> str:
		"""Implementation of the Gauss algorithm to find Easter

		Doesn't work before 1582!

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
			easter = str(year) + "-04-19"
		# Another corner case,
		# when D is 28
		elif ((D == 28) and (E == 6)):
			easter = str(year) + "-04-18"
		else:
			# If days > 31, move to April
			# April = 4th Month
			if (days > 31):
				easter = str(year) + "-04-" + str(days - 31)
			else:
				# Otherwise, stay on March
				# March = 3rd Month
				easter = year +"-03-" + str(days)
		easter_datetime: datetime = datetime.strptime(easter, "%Y-%m-%d")
		return easter_datetime.strftime("%Y-%#m-%#d")


	def _easter_monday(self, year) -> str:
		easter: str = self._easter(year)
		easter_monday_date: datetime = datetime.strptime(easter, "%Y-%m-%d") + timedelta(days=1)
		return easter_monday_date.strftime("%Y-%#m-%#d")
	
	def _add_easter_holidays(self, year: str) -> None:
		easter: str = self._easter(year=year)
		easter_monday: str = self._easter_monday(year=year)
		easter = easter[5:]
		easter_monday = easter_monday[5:]
		holidays_dict[easter] = "Easter Sunday"
		holidays_dict[easter_monday] = "Easter Monday"

holydays = ItalianHolidays()
print(holydays.is_holiday('1787-01-01'))
print(holydays.holiday_name('1061-12-8'))