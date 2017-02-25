# v0.5

# Import Resources
import csv
import argparse
import os
import sys
import platform

# Configure argparse
parser = argparse.ArgumentParser(prog='CSVtoSQL', description='CSVtoSQL is a utility to generate different Oracle SQL scripts by referencing .csv files.')
parser.add_argument('command', choices=['INSERT', 'MERGE'], help='Select the type of statement you would like to generate.')
parser.add_argument('-c', '--commit', help='Prohibits CSVtoSQL from appeninding "COMMIT;" command to the end of the script.', action='store_false')
parser.add_argument('-f', '--filepath', nargs=1, help='Path to csv file (for single file process) or directory with multiple csv files (for batch process).', metavar='csvfile', required=True)
parser.add_argument('-l', '--last', nargs=1, metavar='number of row to limit', help='Limit generation to number of rows defined, starting from end of csv.', default=[0])
parser.add_argument('-t', '--table', nargs=1, metavar='tablename', help='Use this flag to define the name of the table.  (Default: Table Name = Filename without extention)')
args = parser.parse_args()

# Determine Platform Operating System
operating_system = platform.system()

if args.command == "INSERT":
	if os.path.isdir(args.filepath[0]):
		# Get Info About Files To Be Merged
		folder_path_to_files = args.filepath[0]	
		csv_files = os.listdir(folder_path_to_files)
		limit_generation_by = int(args.last[0])
		if len(csv_files) == 0:
			# Exit If No Files In Directory
			print("[Error]: There are no files in the directory provided.")
			sys.exit()
		else:
			for file in csv_files:
				if not file.startswith( '.' ):
					# Set User-Defined Argument Variables
					if args.table is None:
						# Sets the table name as the filename without the file extension
						table_name = os.path.splitext(os.path.basename(file))[0]
					else:
						table_name = args.table[0]
				
					if operating_system == 'Darwin':
						file_name = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/output-' + table_name + '.sql')
						sql_placeholder_file_path = 'INSERT/statement.txt'
						path_to_csv_file = os.path.abspath(folder_path_to_files) + '/' + file
					else:
						file_name = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + '\\Desktop\output-' + table_name + '.sql'
						sql_placeholder_file_path = 'INSERT\statement.txt'
						path_to_csv_file = os.path.abspath(folder_path_to_files) + '\\' + file
				
					# Create File
					with open(file_name, "wt") as outfile:
						outfile.close
					
					# Get SQL INSERT Script Placeholder
					sql_placeholder = open(sql_placeholder_file_path, "rt")
					sql_placeholder_data = sql_placeholder.read()
					sql_placeholder.close()
				
					# Open CSV and build dictionary
					with open(path_to_csv_file, newline='') as csvfile:
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
					if args.commit:
						with open(file_name, "at") as outfile:
							outfile.write('COMMIT;')
							outfile.close
	else:
		# Set User-Defined Argument Variables
		if args.table is None:
			# Sets the table name as the filename without the file extension
			table_name = os.path.splitext(os.path.basename(args.filepath[0]))[0]
		else:
			table_name = args.table[0]
		csv_sql_data = args.filepath[0]
		limit_generation_by = int(args.last[0])

		# Configure OS Specific Variables
		if operating_system == 'Darwin':
			file_name = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/insert-' + table_name + '.sql')
			sql_placeholder_file_path = 'INSERT/statement.txt'
		elif operating_system == 'Windows':
			file_name = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + '\\Desktop\insert-' + table_name + '.sql'
			sql_placeholder_file_path = 'INSERT\statement.txt'

		# Create File
		with open(file_name, "wt") as outfile:
			outfile.close
	
		# Get SQL INSERT Script Placeholder
		sql_placeholder = open(sql_placeholder_file_path, "rt")
		sql_placeholder_data = sql_placeholder.read()
		sql_placeholder.close()
	
		# Open CSV and build dictionary
		with open(csv_sql_data, newline='') as csvfile:
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
		if args.commit:
			with open(file_name, "at") as outfile:
				outfile.write('COMMIT;')
				outfile.close
	
	# Print Success To User
	print('\nCSVtoSQL Completed Sucessfully - Check your desktop for the completed script at insert-' + table_name + '.sql')

elif args.command == "MERGE":
	
	# Configure OS Specific Variables
	if operating_system == 'Darwin':
		file_name = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/merged-script.sql')
	elif operating_system == 'Windows':
		file_name = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + '\\Desktop\merged-script.sql'
	
	# Get Info About Files To Be Merged
	folder_path = args.filepath[0]
	try:
		files_to_merge = os.listdir(folder_path)
	except NotADirectoryError:
		print("[Error]: The file path provided is not a directory. Please check the file path and run again.")
		sys.exit()

	if len(files_to_merge) == 0:
		# Exit If No Files In Directory
		print("[Error]: There are no files in the directory provided.")
		sys.exit()
	else:
		# Create Merged Script File
		with open(file_name, "wt") as outfile:
			outfile.close
			
		for file in files_to_merge:
			if not file.startswith( '.' ):
				if operating_system == 'Darwin':
					path_to_file = os.path.abspath(folder_path) + '/' + file
				else:
					path_to_file = os.path.abspath(folder_path) + '\\' + file
				file_to_be_merged = open(path_to_file, "rt")
				file_contents = file_to_be_merged.read()
				file_to_be_merged.close()
		
				with open(file_name, "at") as outfile:
					outfile.write('/* '+ file + ' */ \n\n' + file_contents + '\n\n\n')
					outfile.close
		
		# Write INSERT Commit
		if args.commit:
			with open(file_name, "at") as outfile:
				outfile.write('COMMIT;')
				outfile.close
				
	# Print Success To User
		print('\nCSVtoSQL Completed Sucessfully - Check your desktop for the completed script at merged-script.sql')