# v0.3.3

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
parser.add_argument('-l', '--last', nargs=1, help='Limit generation to number of rows defined, starting from end of csv.', default=[0])
args = parser.parse_args()

# Set User-Defined Arg Variables
table_name = args.table[0]
data_to_update = args.file[0]
limit_generation_by = int(args.last[0])

# Determine Platform Operating System
operating_system = platform.system()

# Configure OS Specific Variables
if operating_system == 'Darwin':
	file_name = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/output-' + table_name + '.sql')
	sql_placeholder_file_path = 'INSERT/statement.txt'
elif operating_system == 'Windows':
	file_name = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + '\\Desktop\output-' + table_name + '.sql'
	sql_placeholder_file_path = 'INSERT\statement.txt'

if args.command == "INSERT":

	# Create File
	with open(file_name, "wt") as outfile:
		outfile.close
	
	# Get SQL INSERT Script Placeholder
	sql_placeholder = open(sql_placeholder_file_path, "rt")
	sql_placeholder_data = sql_placeholder.read()
	sql_placeholder.close()
	
	# Open CSV and build dictionary
	with open(data_to_update, newline='') as csvfile:
		csv_dictionary = csv.DictReader(csvfile)
		cvs_field_keys = csv_dictionary.fieldnames
		row_values_list = []
		csv_field_names = ''
		
		# Create String of Field Names
		for field_name in cvs_field_keys:
			csv_field_names += field_name
			# Skip comma if last item in array
			if field_name != cvs_field_keys[-1]:
				csv_field_names += ', '
		
		for row in csv_dictionary:
			x = 0
			items = []
			column_value = ''
			replace_column_names = ''
			replace_column_names = sql_placeholder_data.replace("<COLUMN_NAMES>", csv_field_names)
			
			for field_name in cvs_field_keys:
				field_value = row[cvs_field_keys[x]]
				if field_value == '':
					field_value = 'null'
				if field_value.endswith("'") and not field_value.startswith("'") :
					field_value = "'" + field_value
				items.append(field_value)
				# Skip comma if last item in array
				if field_name != cvs_field_keys[-1]:
					items.append(', ')
				x = x + 1
			
			column_value = ''.join(items)
			row_values_list.append(column_value)

		# Generate 
		for row_item in row_values_list[-limit_generation_by:]:
			column_values = ''
			merged_column_values = ''.join(row_item)
			column_values += merged_column_values
			replace_values_in_statement = replace_column_names.replace("<COLUMN_VALUES>", column_values)
			replace_table_in_statement = replace_values_in_statement.replace("<TABLE_NAME>", table_name)
			
			# Write INSERT wrap up
			with open(file_name, "at") as outfile:
				outfile.write(replace_table_in_statement + '\n')
				outfile.close
				
	# Write INSERT Commit
	with open(file_name, "at") as outfile:
		outfile.write('COMMIT;')
		outfile.close
	
	# Print Success To User
	print('\nCSVtoSQL Completed Sucessfully - Check your desktop for the completed script at output-' + table_name + '.sql')