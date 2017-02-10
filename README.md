# CSVtoSQL

CSVtoSQL is a utility to generate different Oracle SQL scripts from data in .csv files.

## Output

```
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (1, 'Kabul', 'AFG', 'Kabol', 1780000);
INSERT INTO USERS (ID, Name, Country Code, District, Population) VALUES (2, 'Qandahar', 'AFG', 'Qandahar', 237500);
COMMIT;
```

## Setup

1. Install Python version 3.0 or later.
2. Clone (or download) the CSVtoSQL repository to your working directory.

```
git clone https://github.com/spetykowski/sql-script-generator.git
```

## Usage

```
py csvtosql.py INSERT -t TABLENAME -f path/to/file.csv
```

### CSV Format
The first row of the csv should exactly match the column name of the target table.

```
ID,Name,Country Code,District,Population
1,'Kabul','AFG','Kabol',1780000
2,'Qandahar','AFG','Qandahar',237500
```

### Supported Data Types

```
String = 'String'
Integer = 1
Decimal = 12.55
Date = TO_DATE('2017/02/06', 'yyyy/mm/dd')
```

### Parameters
CSVtoSQL has a total of 4 parameters (3 required and 1 optional) available.

```
command {INSERT} | (required) Currently CSVtoSQL only supports generating INSERT statements
-t, --table | (required) The Oracle SQL table where the data is 
-f, --file | (required) File path to the .csv document which contains the data to be used in generation
-l, --last | (optional) Used to limit the number of records returned. Will return only the last `n` records.
```

## Example

**via Terminal:**
```
python3 csvtosql.py INSERT -t USERS -f /example/sample.csv
```

**via Powershell:**
```
py .\csvtosql.py INSERT -t USERS -f .\example\sample.csv
```