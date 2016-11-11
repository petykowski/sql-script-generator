titles = open("titlelist.txt", "rt")
titledata = titles.readlines()
titles.close()

values = open("valuelist.txt", "rt")
valuedata = values.readlines()
values.close()

sqlplaceholder = open("placeholderscript.sql", "rt")
sqldata = sqlplaceholder.read()
sqlplaceholder.close()

index = 0

for line in titledata:
	replacetitle = sqldata.replace("VAR_LABEL", line.rstrip())
	replacevalue = replacetitle.replace("VAR_VALUE", valuedata[index].rstrip())
	index += 1
	replacecount = replacevalue.replace("VAR_COUNT", str(index))
	with open("output.sql", "at") as outfile:
		outfile.write(replacecount + '\n')
	outfile.close