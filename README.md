# CSVtoSQL

CSVtoSQL is a utility to generate different Oracle SQL scripts from data in .csv files.

## Output

```SQL
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (1, 'Kabul', 'AFG', 'Kabol', 1780000);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (2, 'Qandahar', 'AFG', 'Qandahar', 237500);
COMMIT;
```

## Setup

1. Install Python version 3.0 or later.
2. Clone (or download) the CSVtoSQL repository to your working directory.

```Shell
git clone https://github.com/spetykowski/sql-script-generator.git
```

## Usage

```Shell
python csvtosql.py INSERT -t TABLENAME -f path/to/file.csv
```

### CSV Format
The first row of the csv should exactly match the column name of the target table.

```
ID,Name,Country Code,District,Population
1,'Kabul','AFG','Kabol',1780000
2,'Qandahar','AFG','Qandahar',237500
```

### Filename
The filename should exactly match that of the SQL table where the generated script will be used. If you would like to define a table name that is different from the filename use the `-t` flag.

### Supported Data Types

```
String = 'String'
Integer = 1
Decimal = 12.55
Date = TO_DATE('2017/02/06', 'yyyy/mm/dd')
```

### Parameters
CSVtoSQL has a total of 5 parameters (2 required and 3 optional) available.

```
command {INSERT} | (required) Currently CSVtoSQL only supports generating INSERT statements.
-c, --commit | (optional) Use this flag to prohibit CSVtoSQL from appending "COMMIT;" to the end of the SQL script.
-f, --file | (required) File path to the .csv document which contains the data to be used in generation.
-l, --last | (optional) Used to limit the number of records returned. Will return only the last `n` records.
-t, --table | (optional) The Oracle SQL table where the data will be manipulated. (Default: Table Name = Filename without extention)
```

## Examples

**via Terminal:**
```Shell
python csvtosql.py INSERT -f example/SQL_SAMPLE.csv
```
```SQL
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (1, 'Kabul', 'AFG', 'Kabol', 1780000);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (2, 'Qandahar', 'AFG', 'Qandahar', 237500);
...
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (9, 'Eindhoven', 'NLD', 'Noord-Brabant', 201843);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (10, 'Tilburg', 'NLD', 'Noord-Brabant', 193238);
COMMIT;
```

**via Powershell:**
```Shell
python csvtosql.py INSERT -f .\example\SQL_SAMPLE.csv
```
```SQL
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (1, 'Kabul', 'AFG', 'Kabol', 1780000);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (2, 'Qandahar', 'AFG', 'Qandahar', 237500);
...
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (9, 'Eindhoven', 'NLD', 'Noord-Brabant', 201843);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (10, 'Tilburg', 'NLD', 'Noord-Brabant', 193238);
COMMIT;
```

**Define Table Name:**
```Shell
python csvtosql.py INSERT -f example/SQL_SAMPLE.csv -t USERS 
```
```SQL
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (1, 'Kabul', 'AFG', 'Kabol', 1780000);
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (2, 'Qandahar', 'AFG', 'Qandahar', 237500);
...
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (9, 'Eindhoven', 'NLD', 'Noord-Brabant', 201843);
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (10, 'Tilburg', 'NLD', 'Noord-Brabant', 193238);
COMMIT;
```

**Generate Last 2 Rows and Skip Commit Command:**
```Shell
python csvtosql.py INSERT -f example/SQL_SAMPLE.csv -l 2 -c
```
```SQL
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (9, 'Eindhoven', 'NLD', 'Noord-Brabant', 201843);
INSERT INTO SQL_SAMPLE (ID, Name, Country Code, District, Population) VALUES (10, 'Tilburg', 'NLD', 'Noord-Brabant', 193238);
```