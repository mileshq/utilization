import sys
import json

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

# create Timesheets class
# is iterable, implements next
# def __iter__(self): returns Day
# def next(self): returns mon, tue, wed, thu ...

class Timesheet(object):

	def __init__(self, d):
		self.date = d['date']
		self.project = d['project']
		self.state = d['state']
		self.hours = d['hours']

	def __str__(self):
		return json.dumps(self, default=lambda i: i.__dict__)

	def persist(self, db_file=TIMESHEETS_FILE):
		with open(db_file, "a") as fh:
			fh.write(str(self) + "\n")

	@staticmethod
	def read_timesheets(db_file=TIMESHEETS_FILE):
		timesheets = []
		with open(db_file, "r") as fh:
			for line in fh:
				timesheets.append(Timesheet(json.loads(line)))
		return timesheets

	@staticmethod
	def sum_project_hours(timesheets, project='*'):
		return sum([t.hours for t in timesheets
			if project in [t.project, '*']])

	@staticmethod
	def sum_utilized_hours(timesheets):
		return sum(t.hours for t in timesheets
			if t.project not in [LABEL_PTO, LABEL_HOLIDAY, LABEL_TRAINING, LABEL_UNUTILIZED])

def main():
	timesheets = Timesheet.read_timesheets()
	print "Total: {}".format(Timesheet.sum_project_hours(timesheets))
	print "Utilized: {}".format(Timesheet.sum_utilized_hours(timesheets))

	
### NON OBJECT ORIENTED CODE, DEPRECATED ###

def new_hours(date, project, state, hours):
	return {"date": date, "project": project, "state": state, "hours": hours}

# consider sorting on write
def persist_hours(hours, db_file=TIMESHEETS_FILE):
	with open(db_file, "a") as fh:
		json.dump(hours, fh)
		fh.write('\n')

def read_hours(db_file=TIMESHEETS_FILE):
	hours = []
	for line in open(db_file, "r"):
		hours.append(json.loads(line))
	return hours

def get_project_hours(hours, project=None):
	return sum([day['hours'] for day in hours
		if is_project(project, day['project'])])

def get_state_hours():
	pass

# consider writing as a lambda
def is_project(expected, actual):
	if expected is None:
		return True
	return expected == actual

def get_utilized_hours(hours):
	total = get_project_hours(hours)
	pto = get_project_hours(hours, LABEL_PTO)
	holiday = get_project_hours(hours, LABEL_HOLIDAY)
	training = get_project_hours(hours, LABEL_TRAINING)
	utilizable = get_project_hours(hours) - (pto + holiday + training)
	unutilized = get_project_hours(hours, LABEL_UNUTILIZED)
	return utilizable - unutilized

def dummy_data():
	persist_hours(new_hours('3/17', 'Holiday', 'NY', 8))
	persist_hours(new_hours('3/18', 'Lando', 'CO', 8))
	persist_hours(new_hours('3/19', 'Lando', 'CO', 8))
	persist_hours(new_hours('3/20', 'Lando', 'CO', 8))
	persist_hours(new_hours('3/21', 'Lando', 'NY', 8))
	
	persist_hours(new_hours('3/24', 'PTO', 'NY', 8))
	persist_hours(new_hours('3/25', 'PTO', 'NY', 8))
	persist_hours(new_hours('3/26', 'Lando', 'CO', 8))
	persist_hours(new_hours('3/27', 'Lando', 'CO', 8))
	persist_hours(new_hours('3/28', 'Lando', 'NY', 8))	

def _main():
	hours = read_hours()
	print "Total hours: {}".format(get_project_hours(hours))
	print "PTO hours: {}".format(get_project_hours(hours, LABEL_PTO))
	print "Holiday hours: {}".format(get_project_hours(hours, LABEL_HOLIDAY))
	print "Training hours: {}".format(get_project_hours(hours, LABEL_TRAINING))
	print "Utilized: {}".format(get_utilized_hours(hours))

if __name__ == '__main__':
	main()