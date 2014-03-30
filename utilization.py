import sys
import json

# file to store list of hours in json format
HOURS_FILE = "my_hours.json"

# IBB internal project LABELs
LABEL_PTO = "PTO"
LABEL_HOLIDAY = "Holiday"
LABEL_TRAINING = "Training"
LABEL_UNUTILIZED = "Unutilized"

# not used yet
HOLIDAY_DAYS = ['1/1', '1/20', '2/17', '5/26', '7/4', '9/1', '11/27', '11/28', '12/25', '12/26']
HOLIDAY_DAYS_COUNT = len(HOLIDAY_DAYS)
PTO_DAYS_COUNT = 20

def new_hours(date, project, state, hours):
	return {"date": date, "project": project, "state": state, "hours": hours}

def persist_hours(hours, db_file=HOURS_FILE):
	with open(db_file, "a") as fh:
		json.dump(hours, fh)
		fh.write('\n')

def read_hours(db_file=HOURS_FILE):
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

# create a class for data structure
# read in list of classes
# create new class from command line args
# add serialize method on class - write itself from a file, then read itself from file
# class knows how to persist itself

# create timesheet class, holds 7 days
# is iterable, implements next
# def __iter__(self): returns Day
# def next(self): returns mon, tue, wed, thu ...

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

def main():
	hours = read_hours()
	#print hours
	print "Total hours:    {}".format(get_project_hours(hours))
	print "PTO hours:      {}".format(get_project_hours(hours, LABEL_PTO))
	print "Holiday hours:  {}".format(get_project_hours(hours, LABEL_HOLIDAY))
	print "Training hours: {}".format(get_project_hours(hours, LABEL_TRAINING))

	print "Utilized: {}".format(get_utilized_hours(hours))
if __name__ == '__main__':
	main()