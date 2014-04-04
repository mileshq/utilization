import sys
import json
import argparse
from datetime import date

# file to store list of hours in json format
TIMESHEETS_FILE = "my_timesheets.json"

# IBB internal project LABELs
LABEL_PTO = "PTO"
LABEL_HOLIDAY = "Holiday"
LABEL_TRAINING = "Training"
LABEL_UNUTILIZED = "Unutilized"

# not used yet
HOLIDAY_DAYS = ['1/1', '1/20', '2/17', '5/26', '7/4', '9/1', '11/27', '11/28', '12/25', '12/26']
HOLIDAY_DAYS_COUNT = len(HOLIDAY_DAYS)
PTO_DAYS_COUNT = 20

class TimesheetEntry(object):

	def __init__(self, date, project, state, hours):
		self.date = date
		self.project = project
		self.state = state
		self.hours = hours

	# __repr__ instead ?
	def __str__(self):
		return json.dumps(self, default=lambda i: i.__dict__)

	def persist(self, db_file=TIMESHEETS_FILE):
		with open(db_file, "a") as fh:
			fh.write(str(self) + "\n")

class Timesheets(object):

	def __init__(self, db_file=TIMESHEETS_FILE):
		self.timesheets = []
		with open(db_file, "r") as fh:
			for line in fh:
				self.timesheets.append(TimesheetEntry(**json.loads(line)))

	def add_timesheet_entry(self, timesheet_entry):
		self.timesheets.append(timesheet_entry)

	def sum_project_hours(self, project='*'):
		return sum([t.hours for t in self.timesheets
			if project in [t.project, '*']])

	def sum_utilized_hours(self):
		return sum(t.hours for t in self.timesheets
			if t.project not in [LABEL_PTO, LABEL_HOLIDAY, LABEL_TRAINING, LABEL_UNUTILIZED])

	# this could be more efficient
	def percent_utilized_hours(self):
		return float(self.sum_utilized_hours()) / float(self.sum_project_hours()) * 100

	# def __iter__(self): returns TimesheetEntry
	# is iterable, implements next()
	# might be pythonic way to do interation below in persist
	def persist(self, db_file=TIMESHEETS_FILE):
		with open(db_file, 'w') as fh:
			for t in self.timesheets:
					fh.write(str(t) + "\n")

def parse_args():
	parser = argparse.ArgumentParser(description="Capture and confirm utilization.")	
	#exclusive_group = parser.mutually_exclusive_group()
	add_entry_group = parser.add_argument_group()
	add_entry_group.add_argument('-a', '--add', help='Add new timesheet entry.')
	add_entry_group.add_argument('date')
	add_entry_group.add_argument('project')
	add_entry_group.add_argument('state')
	add_entry_group.add_argument('hours', type=int, default=8)
	#parser.add_argument(dest='day_count')

	args = parser.parse_args()
	
	if args.add:
		return TimesheetEntry(**args.__dict__)
		

def main():
	timesheets = Timesheets()
	print "Loaded {} timesheets.".format(len(timesheets.timesheets))
	new_timesheet = parse_args()
	print "Adding new timesheet: {}".format(new_timesheet.__dict__)
	add_timesheet_entry(new_timesheet)
	print "Total timesheets: {}".format(len(timesheets.timesheets))

	#timesheets.timesheets.sort()
	#print timesheets.timesheets
	#parse_args()

	print "Total: {}".format(timesheets.sum_project_hours())
	print "Utilized: {}".format(timesheets.sum_utilized_hours())
	print "Utilized: {}%".format(timesheets.percent_utilized_hours())

if __name__ == '__main__':
	main()
