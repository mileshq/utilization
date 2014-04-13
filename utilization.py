import sys
import json
import argparse
import datetime

# TODO: move to yaml configuration file

# file to store list of hours in json format
TIMESHEETS_FILE = "my_timesheets.json"

# IBB internal WBS codes
WBS_PTO = "PTO"
WBS_HOLIDAY = "Holiday"
WBS_TRAINING = "Training"
WBS_UNUTILIZED = "Unutilized"
WBS_IBB = [WBS_PTO, WBS_HOLIDAY, WBS_TRAINING, WBS_UNUTILIZED]

# Client project WBS codes
WBS_PROJECTS = ['Lando']

# Valid WBS codes
VALID_WBS = WBS_PROJECTS + WBS_IBB

# Allocated PTO per year
PTO_HOURS_COUNT = 20 * 8

# not used yet
HOLIDAY_DAYS = ['1-1', '1-20', '2-17', '5-26', '7-4', '9-1', '11-27', '11-28', '12-25', '12-26']
HOLIDAY_HOURS_COUNT = len(HOLIDAY_DAYS) * 8

VALID_STATES = ['NY', 'PA', 'CO']
CURRENT_YEAR = 2014

class TimesheetRecord(object):

	def __init__(self, date, project, state, hours):
		self.date = TimesheetRecord.valid_date(date)
		self.project = TimesheetRecord.valid_project(project)
		self.state = TimesheetRecord.valid_state(state)
		self.hours = TimesheetRecord.valid_hours(hours)

	# __repr__ instead ?
	def __str__(self):
		#return json.dumps(self, default=lambda i: i.__dict__)
		return json.dumps({'date': str(self.date), 'project': self.project,
			'state': self.state, 'hours': self.hours})

	def append_to_file(self, db_file=TIMESHEETS_FILE):
		with open(db_file, "a") as fh:
			fh.write(str(self) + "\n")

	@staticmethod
	def valid_date(date):
		d = [int(d) for d in date.replace('/', '-').split('-')]
		if len(d) == 2:
			return datetime.date(CURRENT_YEAR, *d)
		if len(d) == 3:
			return datetime.date(*d)
		raise ValueError('Invalid date.')

	@staticmethod
	def valid_project(project):
		#return project in VALID_PROJECTS
		if project in WBS_PROJECTS + WBS_IBB:
			return project
		raise ValueError('Invalid project.')

	@staticmethod
	def valid_state(state):
		#return state in VALID_STATES
		s = state.upper()
		if s in VALID_STATES:
			return s
		raise ValueError('Invalid state.')
	
	@staticmethod
	def valid_hours(hours):
		h = float(hours)
		if h > 0 and h < 24:
			return h
		raise ValueError('Invalid hours.')


class Timesheets(object):

	def __init__(self, db_file=TIMESHEETS_FILE):
		self.timesheets = []
		with open(db_file, "r") as fh:
			for line in fh:
				#print json.loads(line)['date'].split('-')
				self.timesheets.append(TimesheetRecord(**json.loads(line)))

	def add_timesheet_entry(self, timesheet_entry):
		self.timesheets.append(timesheet_entry)

	def sum_project_hours(self, project='*'):
		return sum([t.hours for t in self.timesheets
			if project in [t.project, '*']])

	def sum_utilized_hours(self):
		return sum(t.hours for t in self.timesheets
			if t.project not in WBS_IBB)

	# this could be more efficient
	def percent_utilized_hours(self):
		return float(self.sum_utilized_hours()) / float(self.sum_project_hours()) * 100

	def remain_pto_hours(self):
		return PTO_HOURS_COUNT - self.sum_project_hours(WBS_PTO)

	def utilized_projects(self):
		return set([t.project for t in self.timesheets
			if t.project not in WBS_IBB])

	# def __iter__(self): returns TimesheetEntry
	# is iterable, implements next()
	# might be pythonic way to do interation below in persist
	def persist(self, db_file=TIMESHEETS_FILE):
		with open(db_file, 'w') as fh:
			for t in self.timesheets:
					fh.write(str(t) + "\n")

# consider this form
# $ utilization.py 3/21 4 l2 CO 8
def main():
	parser = argparse.ArgumentParser(description="Capture and report utilization.")	
	ex_group = parser.add_mutually_exclusive_group(required=False)
	ex_group.add_argument('-a', '--add', nargs=4,
		metavar=('date', 'project', 'state', 'hours'), help='Add new timesheet entry.')
	ex_group.add_argument('-r', '--report', action='store_true', 
		help='Report current utilization.')
	ex_group.add_argument('-l', '--list', action='store_true', 
		help='Print all timesheet records.')

	args = parser.parse_args()
	print args

	if args.add:
		try:
			t = TimesheetRecord(*args.add)
			print t.__dict__
			#timesheets.add_timesheet_entry(t)
		except ValueError as te:
			print te

	if args.report:
		timesheets = Timesheets()
		pto_hours = timesheets.remain_pto_hours()
		print "Remaining PTO: {} days ({} hours)".format(pto_hours / 8, pto_hours)
		print "Utilized: {}%".format(timesheets.percent_utilized_hours())
		print "Projects: {}".format(", ".join(timesheets.utilized_projects()))

	if args.list:
		timesheets = Timesheets()
		for t in timesheets.timesheets:
			print t

if __name__ == '__main__':
	main()
