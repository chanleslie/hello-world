import re 

def decimalat(DegString):
	
	SearchStr='(\d+) ([\d\.]+) (\w)'
	Result = re.search(SearchStr, DegString)

	Degrees = float(Result.group(1))
	Minutes = float(Result.group(2))
	Compass = Result.group(3).upper() 

	DecimalDegree = Degrees + Minutes/60

	if Compass == 'S' or Compass == 'W':
		DecimalDegree = -DecimalDegree  
	return DecimalDegree

InFileName = 'Marrus_claudanielis.txt'

OutFileName = 'dec_' + InFileName

WriteOutFile = True

InFile = open(InFileName, 'r')

HeaderLine = 'dive\tdepth\tlatitude\tlongitude\tdate\tcomment'
print(HeaderLine)

if WriteOutFile:

	OutFile = open(OutFileName, 'w')
	OutFile.write(HeaderLine + '\n')


LineNumber = 0

for Line in InFile:
	
	if LineNumber > 0:
		
		Line=Line.strip('\n')
		ElementList = Line.split('\t')
	
		Dive    = ElementList[0]
		Date    = ElementList[1]
		Depth   = ElementList[4]
		Comment = ElementList[5]

		LatDegrees = decimalat(ElementList[2])
		LonDegrees = decimalat(ElementList[3])
		
		OutString = "%s\t%4s\t%10.5f\t%10.5f\t%9s\t%s" % \
                         (Dive,Depth,LatDegrees,LonDegrees,Date,Comment)
		print(OutString)
		if WriteOutFile:
			OutFile.write(OutString + '\n') 
		
	LineNumber += 1 
	
InFile.close()
if WriteOutFile:
	OutFile.close()