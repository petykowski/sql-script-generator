# v0.3.1

# Import Resources
import csv
import argparse
import os
import platform

# Configure argparse
parser = argparse.ArgumentParser(prog='CSVtoSQL', description='CSVtoSQL is a utility to generate different Oracle SQL scripts by referencing .csv files.')
parser.add_argument('command', choices=['INSERT'], help='Select the type of statement you would like to generate.')
parser.add_argument('-f', '--file', nargs=1, help='File path to csv file.', required=True)
parser.add_argument('-t', '--table', nargs=1, help='Use this flag to define the name of the table', required=True)
args = parser.parse_args()

# Determine Platform OS
platform = platform.system()

# Get User Desktop
if platform == 'Darwin':
	Filename = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/output.sql')
elif platform == 'Windows':
	Filename = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop\output.sql"
	
# Set File Paths
if platform == 'Darwin':
	sqlplaceholderfilepath = 'INSERT/statement.txt'
elif platform == 'Windows':
	sqlplaceholderfilepath = 'INSERT\statement.txt'
	
datatoupdate = args.file[0]

if args.command == "INSERT":

	# Create File
	with open(Filename, "wt") as outfile:
		outfile.close

	# Set Table Name
	tablename = args.table[0]
	
	# Get SQL INSERT Script Placeholder
	sqlplaceholder = open(sqlplaceholderfilepath, "rt")
	sqldata = sqlplaceholder.read()
	sqlplaceholder.close()
	
	# Open CSV and build dictionary
	with open(datatoupdate, newline='') as csvfile:
		dictcsv = csv.DictReader(csvfile)
		fields = dictcsv.fieldnames

		fieldnames = ''
		
		for field in fields:
			fieldnames += field
			if field != fields[-1]:
				fieldnames += ', '
		
		for row in dictcsv:
			x = 0
			items = ''
			replaceColumnNames = ''
			replaceColumnNames = sqldata.replace("<COLUMN_NAMES>", fieldnames)
			
			for field in fields:
				checkitem = row[fields[x]]
				if checkitem == '':
					checkitem = 'null'
				if checkitem.endswith("'"):
					checkitem = "'" + checkitem
				items += checkitem
				if field != fields[-1]:
					items += ', '
				x = x + 1
					
			replaceItems = replaceColumnNames.replace("<COLUMN_VALUES>", items)
			replaceTable = replaceItems.replace("<TABLE_NAME>", tablename)
	
			# Write INSERT wrap up
			with open(Filename, "at") as outfile:
				outfile.write(replaceTable + '\n')
				outfile.close
				
	# Write INSERT Commit
	with open(Filename, "at") as outfile:
		outfile.write('COMMIT;')
		outfile.close
	
	print('\nCSVtoSQL Completed Sucessfully - Check your desktop for the completed script at output.sql')