# final1.py
# 111a-an Sam Scharr
# 
# Main site: http://www.metoffice.gov.uk/climate/uk/stationdata/
# This program uses data from the above stated website to answer
# various questions concerning weather in England.
#
import urllib2
import sys
 
URL = "http://www.metoffice.gov.uk/climate/uk/stationdata/"

cities = {'Aberporth'           :   'aberporthdata.txt' ,
          'Armagh'              :   'armaghdata.txt' ,
          'Ballypatrick Forest' :   'ballypatrickdata.txt' ,	 
          'Bradford'            :   'bradforddata.txt' ,
          'Braemar'             :   'braemardata.txt' ,
          'Camborne'	        :   'cambornedata.txt' ,
          'Cambridge NIAB'      :   'cambridgedata.txt' ,
          'Cardiff Bute Park'   :   'cardiffdata.txt' ,
          'Chivenor' 	        :   'chivenordata.txt' ,
          'Cwmystwyth'	        :   'cwmystwythdata.txt' ,
          'Dunstaffnage'        :   'dunstaffnagedata.txt' ,
          'Durham'	        :   'durhamdata.txt' ,
          'Eastbourne'	        :   'eastbournedata.txt' ,
          'Eskdalemuir'	        :   'eskdalemuirdata.txt' ,
          'Heathrow'	        :   'heathrowdata.txt' ,
          'Hurn'	        :   'hurndata.txt' ,
          'Lerwick'	        :   'lerwickdata.txt' ,
          'Leuchars'	        :   'leucharsdata.txt' ,
          'Lowestoft'	        :   'lowestoftdata.txt',
          'Manston'	        :   'manstondata.txt',
          'Nairn'	        :   'nairndata.txt',
          'Newton Rigg'	        :   'newtonriggdata.txt',
          'Oxford'	        :   'oxforddata.txt',
          'Paisley'	        :   'paisleydata.txt',
          'Ringway'	        :   'ringwaydata.txt',
          'Ross-on-Wye'	        :   'rossonwyedata.txt',
          'Shawbury'	        :   'shawburydata.txt',
          'Sheffield'	        :   'sheffielddata.txt',
          'Southampton'	        :   'southamptondata.txt',
          'Stornoway Airport'   :   'stornowaydata.txt',
          'Sutton Bonington'    :   'suttonboningtondata.txt',
          'Tiree'	        :   'tireedata.txt',
          'Valley'	        :   'valleydata.txt',
          'Waddington'	        :   'waddingtondata.txt',
          'Whitby'	        :   'whitbydata.txt',
          'Wick Airport'        :   'wickairportdata.txt',
          'Yeovilton'	        :   'yeoviltondata.txt',     }


# This allows the program to open and read the website.
def getCityInfo( fileName ):
   global URL
   f = urllib2.urlopen( URL + fileName )
   bytes = f.read()
   htmlText  = bytes.decode( "utf8" )
   return htmlText

# This retreives the earliest year recorded for each city.
def getEarliest( text ):
    for line in text.split( '\n' ):
        if len( line )>1 and line[0]==' ':
            try:
                year = eval( line.split()[0] )
                month = eval( line.split()[1] )
                return year, month
            except NameError:
                continue
    return None, None

# This gets the month and year that the earliest info is recorded at.
def oldestInfo( earliestTemps ):
   earliestTemps1 = []
   earliestTemps.sort()
   earliest = earliestTemps[0]
   earliestYear = earliest[0]
   earliestMonth = earliest[1]
   for year, month, city in earliestTemps:
         if year == earliestYear and month == earliestMonth:
            earliestTemps1.append( [year, month, city] )
         else:
            continue
         
   return earliestTemps1

# This converts a numerical month into the name of that month.
def findMonth( month ):
   monthsTable = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]
 
   # if month is 1, get monthsTable[0], which is "Jan".  Same for 2, get "Feb", etc.
   month = monthsTable[ month -1 ]
   
   return month

# This finds the maximum temperature recorded with the month and
# year for each city.
def findMaxTemp( text ):
   maxTemps = []
   for line in text.split( '\n' ):
        if len( line )>1 and line[0]==' ':
            try:
                year = eval( line.split()[0] )
                month = eval( line.split()[1] )
                temp = eval( line.split()[2] )
                maxTemps.append( [temp, month, year] )
            except (NameError, SyntaxError):
                continue
   maxTemps.sort()
   maxTemp, maxMonth, maxYear = maxTemps[-1]
   return maxTemp, maxMonth, maxYear

# This finds the maximum temperature recorded with the month and
# year for each city.
def findMinTemp( text ):
   minTemps = []
   for line in text.split( '\n' ):
        if len( line )>1 and line[0]==' ':
            try:
                year = eval( line.split()[0] )
                month = eval( line.split()[1] )
                temp = eval( line.split()[3] )
                minTemps.append( [temp, month, year] )
            except (NameError, SyntaxError):
                continue
   minTemps.sort()
   minTemp, minMonth, minYear = minTemps[0]
   
   return minTemp, minMonth, minYear

# This converts the temperature from celcius to farenheit. 
def convertTemp( tempC ):
   tempF = (9/5) * tempC + 32
   return tempF

# This calculates the average sun exposure each city gets.
def sunExpo( text ):
   sunExp = []
   sunExp1 = []
   for line in text.split( '\n' ):
      if len( line )>1 and line[0]==' ':
         try:
            sun = line.split()[6]
            sunExp.append( sun )
         except (NameError, SyntaxError, IndexError):
               continue

   for sun in sunExp:
      try:
         sunExp1.append( eval(sun))
      except (NameError, SyntaxError):
         if '*' in sun:
            sun = sun[:-1]
            sunExp1.append( eval(sun))
         elif '#' in sun:
            sun = sun[:-1]
            sunExp1.append( eval(sun))
         continue

   totalSun = 0
   for sun in sunExp1:
      try:
         totalSun = totalSun + sun
      except TypeError:
         continue

   avgSun = totalSun/len(sunExp1)
      
   return avgSun

# This calculates the average temperature for each half of the 20th
# century for each city. 
def avgTemps( text ):
   allTemps = []
   firstHalf = []
   secondHalf = []
   for line in text.split( '\n' ):
      if len( line )>1 and line[0]==' ':
         try:
            year = eval( line.split()[0] )
            tmax = eval( line.split()[2] )
            tmin = eval( line.split()[3] )
            allTemps.append( [year, tmax, tmin] )
         except (NameError, SyntaxError):
            continue
   # Splits the recorded temperatures between the first and second halves.
   for year, tmax, tmin in allTemps:
      if 1900 <= year and year < 1950:
         firstHalf.append( tmin )
         firstHalf.append( tmax )
      elif 1950 <= year and year < 2000:
         secondHalf.append( tmin )
         secondHalf.append( tmax )
      else:
         continue

   # Calculates the average for each half, first by adding together all
   # the temperatures, then dividing that total by the number of temps
   # added together.
   fTotal = 0
   for temp in firstHalf:
      fTotal = fTotal + temp

   sTotal = 0
   for temp in secondHalf:
      sTotal = sTotal + temp

   try:
      fAvg = fTotal/len(firstHalf)
   except ZeroDivisionError:
      fAvg = 0

   try:
      sAvg = sTotal/len(secondHalf)
   except ZeroDivisionError:
      sAvg = 0
        
   return fAvg, sAvg

def yearlyDif( text ):
   # Find the temperature difference for each year.
   # Collect the temperature data for each year.
   temps = []
   for line in text.split( '\n' ):
      if len( line )>1 and line[0]==' ':
         try:
            year = eval( line.split()[0] )
            tmax = eval( line.split()[2] )
            tmin = eval( line.split()[3] )
            temps.append( [year, tmax, tmin] )
         except (NameError, SyntaxError):
            continue
   temps.sort()

   # Sort the data by year using a dictionary. The Key is the year,
   # the values are the temperatures for that year.
   earYear, etmax, etmin = temps[0]
   yeartempdict = {}
   for year, tmax, tmin in temps:
      if year == earYear:
         if year in yeartempdict:
            yeartempdict[year] += tmax, tmin
         else:
            yeartempdict[year] = tmax, tmin
      else:
         earYear += 1
   # Turn the dictionary into a list.
   allTemps = []
   for temps in yeartempdict.keys():
      # Since the values are a tuple, turn values into a list.
      # Source: http://blog.labix.org/2008/06/27/watch-out-for-listdictkeys-in-python-3
      temp = list(yeartempdict[ temps ])
      allTemps.append( [temps, temp] )

   # Find the yearly difference for each year.
   yearlyDif = [] 
   for year, temps in allTemps:
      temps.sort()
      minTemp = temps[0]
      maxTemp = temps[-1]
      tempDif = maxTemp - minTemp
      yearlyDif.append( [tempDif, year] )

   # Sort to find the biggest yearly difference.
   yearlyDif.sort()
   tempDif, year = yearlyDif[-1]
         
   return tempDif, year

   
def main():
   print "Answer to Question 1" 
   # Finds the earliest info for each city.
   earliestTemps = []
   for city in cities.keys():
       year, month = getEarliest( getCityInfo( cities[ city ] ) )
       earliestTemps.append( [year, month, city] )

   # Evaluates all the oldest info to find which city or cities have the
   # oldest records.
   oldest = oldestInfo( earliestTemps)
   for year, month, city in oldest:
      month = findMonth( month )
      print "The oldest observation was recorded in", city, "in", month, "in", year
   

   print "\nAnswer to Question 2" 
   # Finds all the minimum temps for each city
   minTemp = []
   for city in cities.keys():
      minTempC, month, year = findMinTemp( getCityInfo( cities[ city ] ) )
      minTemp.append( [minTempC, month, year, city] )

   # Evaluates each minimum temp to find the lowest.
   minC = [0]
   minimumTemp = []
   for minTempC, month, year, city in minTemp:
      if minTempC <= minC[0]:
         minC.remove( minC[0] )
         minC.append( minTempC )
         minimumTemp.append( [convertTemp(minTempC), findMonth(month), year, city] )
      else:
         continue

   # If list minimumTemp collected more than 1 value, evaluate list for lowest
   # value.
   while len( minimumTemp ) > 1:
      for tempF, month, year, city in minimumTemp:
         if (tempF in minimumTemp[0]) > (tempF in minimumTemp[1]):
            minimumTemp.remove( minimumTemp[0] )
         else:
            minimumTemp.remove( minimumTemp[1] )
          
   for tempF, month, year, city in minimumTemp:
      print "The coldest temperature was", "%0.2f" %(tempF), "degrees F recorded in", city, "in", month, "of", year


   print "\nAnswer to Question 3" 
   # Finds all the maximum temps for each city
   maxTemp = []
   for city in cities.keys():
      maxTempC, month, year = findMaxTemp( getCityInfo( cities[ city ] ) )
      maxTemp.append( [maxTempC, month, year, city] )

   # Evaluates each maximum temp to find the highest.
   maxC = [0]
   maximumTemp = []
   for maxTempC, month, year, city in maxTemp:
      if len(maxC) == 0:
         maximumTemp.append( [convertTemp(maxTempC), findMonth(month), year, city] )
      elif maxTempC > maxC[0]:
         maxC.remove(maxC[0])
         maxC.append( maxTempC )
         maximumTemp.append( [convertTemp(maxTempC), findMonth(month), year, city] )
      else:
         continue

   # If list maximumTemp collected more than 1 value, evaluate list for highest
   # value.
   while len( maximumTemp ) > 1:         
      for tempF, month, year, city in maximumTemp:
         if (tempF in maximumTemp[0]) < (tempF in maximumTemp[1]):
            maximumTemp.remove( maximumTemp[0])
         else:
            maximumTemp.remove( maximumTemp[1])

   for tempF, month, year, city in maximumTemp:
      print "The hottest temperature was", "%0.2f" %(tempF), "degrees F recorded in", city, "in", month, "of", year

   
   print "\nAnswer to Question 4"
   # Parses data to find the biggest yearly difference for each city.
   bigDif = []
   for city in cities.keys():
      biggestDif, year = yearlyDif( getCityInfo( cities[ city ] ) )
      bigDif.append([ biggestDif, year, city ])

   # Organize the data for each city and take the largest value.
   bigDif.sort()
   temp, year, city = bigDif[-1]
   tempF = convertTemp( temp )
   print "The biggest yearly temperature difference was", "%0.2f" % tempF, "degrees F", "in", year, "in", city
      
   
   print "\nAnswer to Question 5"
   # Finds the average sun exposure for each city and puts it in a list.
   sunExp = []
   for city in cities.keys():
      avgSun = sunExpo( getCityInfo( cities[ city ] ) )
      sunExp.append( [ avgSun, city ] )

   # Sorts list of averages and takes the highest. 
   sunExp.sort()
   sun, city = sunExp[-1]

   print "The city with the most sun exposure is", city, "with an average of", "%0.2f" %(sun)

   print "\nAnswer to Question 6"
   fHalf = []
   sHalf = []
   # Gathers the first and second half averages for each city.
   for city in cities.keys():
      firstHalf, secondHalf = avgTemps( getCityInfo( cities[ city ] ) )
      fHalf.append( firstHalf )
      sHalf.append( secondHalf)

   # Adds together all the first half averages and divides by the
   # number of those to get the total average for the first half.
   fHalfAvgTot = 0
   for avg in fHalf:
      try:
         fHalfAvgTot = fHalfAvgTot + avg
      except TypeError:
         continue
   fHalfAvg = fHalfAvgTot/len(fHalf)

   # Adds together all the second half averages and divides by the
   # number of those to get the total average for the second half.
   sHalfAvgTot = 0
   for avg in sHalf:
      try:
         sHalfAvgTot = sHalfAvgTot + avg
      except TypeError:
         continue
   sHalfAvg = sHalfAvgTot/len(sHalf)

   # Converts the temperatures from celcius to farenheit. 
   fHalfF = convertTemp( fHalfAvg )
   sHalfF = convertTemp( sHalfAvg )

   # Prints the correct statement based on which half has the higher average.
   if fHalfF < sHalfF:
      print "The first half of the 20th century was colder than the second half.\n" \
            "The average temperature of the first half was", "%0.2f" %(fHalfF), "degrees F.\n" \
            "The average temperature of the second half was", "%0.2f" %(sHalfF), "degrees F."
   else:
      print "The first half of the 20th century was hotter than the second half.\n" \
            "The average temperature of the first half was", "%0.2f" %(fHalfF), "degrees F.\n" \
            "The average temperature of the second half was", "%0.2f" %(sHalfF), "degrees F."
 
      
main()
