# Useful Variables & Constants
FILENAME = 'input.txt'
DAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
HOURS = [x for x in range(24)]
workers = []
data_schedules = []


def main():
    schedules = getRawData(FILENAME)
    appendSchedules(schedules)
    # Nested loop to check first worker with every other-->second with every other except first and so on
    for i in range(len(workers)):
        j = i + 1
        while(j < len(workers)):
            flag, coincidences, names = checkDaysCoincidences(data_schedules[i],data_schedules[j])
            if(flag):
                print(f'{names} {coincidences}')
            j += 1


# Reads a file. Recieves a filname or route. Returns a list of schedules.
def getRawData(filename):
    # Open the .txt file to read it
    with open(filename, 'r') as file:
        # Read each line
        schedules = file.readlines() # --> ['RENE=MO10:00-..'02:00', 'ASTRID=MO10:00-...', 'ANDRES=MO10:00-...']
        # Strip each element
        schedules = list(map(lambda line: line.strip(), schedules))
        return schedules


# Divides the data. Recieves a list. Does not return. Side effect: Fills data_schedules
def appendSchedules(schedules_list):
    try:
        # Iterate to take name and individial schedule --> split on '=' character
        for schedule in schedules_list:
            worker, workerSchedule = schedule.split('=')
            # Create a dictionary for each worker to link it with its schedule and append it to a list.
            data = {'name': worker, 'days&hours': workerSchedule.split(',') } # --> {'name': 'RENE', 'days&hours': ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00, 'SU01:00-02:00']}
            data_schedules.append(data)
            #Append the worker's name to another list. This will be helpful when iterating to compare schedules
            workers.append(worker)
    #If there is no split in schedule.split('='), the next error will occur: ValueError: not enough values to unpack (expected 2, got 1)
    except ValueError:
        print('Input file does not have the require format')


# Checks if days in schedule match. Recieves two dictionaries with a worker's name and schedule. 
# Returns a bool, an int of the times they had a coincidence in the schedule, and the names of whose schedule match.
def checkDaysCoincidences(worker1, worker2):
    # Building the names string for the requested output
    coincidenceNames = worker1['name'] + '-' + worker2['name'] + ':'
    # Counter of coincidences
    times = 0
    
    # Nested loop to get a day and some information on the hours of that day.
    for w1Day in worker1['days&hours']:
        day1 = w1Day[:2] # e.g --> 'MO'
        start1, end1  = w1Day[2:].split('-') 
        hourDistance1 = abs( int(end1[:2]) - int(start1[:2]) )
        for w2Day in worker2['days&hours']:
            day2 = w2Day[:2]
            start2, end2  = w2Day[2:].split('-')
            hourDistance2 = abs( int(end2[:2]) - int(start2[:2]) )

            # Using the indexes on DAYS list we can identify if its the same day
            dayDistance = DAYS.index(day1) - DAYS.index(day2)
            pack1 = [start1, end1, hourDistance1] # --> e.g ['10:00', '12:00', 2] 
            pack2 = [start2, end2, hourDistance2]
            # checkCoincidencesHours parameters should be ordered according to the distance between their hours for the other functions to work correctly.
            if(hourDistance2 > hourDistance1):
                temp = pack1
                pack1 = pack2
                pack2 = temp
            
            # dayDistance helps the algorithm being more efficient because it recognizes if it keeps comparing or goes to the next day in the list
            # If its the same day, continue checking for coincidence in hours and minutes
            if dayDistance == 0:
                #Now that pack1 and pack2 are sorted:
                if ( checkHoursCoincidences( pack1, pack2) ):
                    times += 1
                break
            # If its a previous day, keep iterating worker2
            elif dayDistance > 0:
                continue
            # If its a following day, stop and go to the next day on worker1
            elif dayDistance < 0:
                break

    #Has coincidences
    if (times > 0):
        return True, times, coincidenceNames
    #No coincidences
    return False, times, coincidenceNames


# Checks the intervals hours in various cases. To see this cases check README.md. 
# Recieves a list with this format: [start1, end1, hourDistance1] # --> e.g ['10:00', '12:00', 2]
# Returns a bool. True if coincidence, False if not
def checkHoursCoincidences(hours1, hours2):
    #Check Case 1.1 and Case 1.2 in README.md
    if(hours1[0] == hours2[0] or hours1[1] == hours2[1]):
        return True

    #Getting the start and end hours of the second worker
    startHour = int(hours2[0][:2])
    endHour = int(hours2[1][:2])
    
    # Interval includes the start and end hours
    interval = getIntervalHours(hours1, hours1[2])
    comparisonStart = startHour in interval
    comparisonEnd = endHour in interval

    # strictInterval does not include the start and end hours
    strictInterval = interval[1:-1]
    strictComparisonStart = startHour in strictInterval 
    strictComparisonEnd = endHour in strictInterval

    # If both hours are in the strictInterval,then there is a coincidence for certain. Check case 3
    if(strictComparisonStart and strictComparisonEnd):
        return True
    #Check Cases 4 and 5
    if(comparisonStart or comparisonEnd):
        if(checkMinutesCoincidences(hours1, hours2)):
            return True
        return False
    else:
        return False


# Creats hour intervals in a list format to use in checkHoursCoincidences
# Recieves a list with this format: [hours] --> e.g ['10:00', '12:00'] and an int
# Returns a list of the input's hour interval --> [10, 11, 12]
def getIntervalHours(hours, hourDistance):
    # Getting start and end hour
    start = int(hours[0][:2])
    end = start + hourDistance
    # Building the interval using the HOURS list
    interval = HOURS[start:end + 1]

    # In case the interval includes 00 inside of it, this part corrects the produced list
    if(len(interval) < hourDistance + 1):
        remaining = hourDistance - len(interval) + 1
        interval += HOURS[:remaining]
    return interval


# Got the idea from: https://stackoverflow.com/questions/45656834/python-compare-date-strings-without-using-built-in-functions-or-libraries
# Recieves two lists with the same format: [hours1] --> e.g ['10:00', '12:00']
# Returns a bool. True if coincidence, False if not
def checkMinutesCoincidences(hours1, hours2):
    # Creates the variables. Converts hours and minuts to ints.
    hourStart1, minStart1 = map(int, hours1[0].split(':'))
    hourEnd1, minEnd1 = map(int, hours1[1].split(':'))

    hourStart2, minStart2 = map(int, hours2[0].split(':'))
    hourEnd2, minEnd2 = map(int, hours2[1].split(':'))

    # Order is important. Turns out if you put the time in the same format, it campares them accurately. 
    # It fails to make the correct comparison if the interval includes the borders of the list HOURS inside of it.
    if((hourStart1, minStart1) > (hourStart2, minStart2)):
        flag1 = (hourEnd2, minEnd2) > (hourStart1, minStart1) > (hourStart2, minStart2)
        flag2 = (hourEnd2, minEnd2) > (hourEnd1, minEnd1) > (hourStart2, minStart2)

        return flag1 or flag2

    else:
        flag1 = (hourEnd1, minEnd1) > (hourStart2, minStart2) > (hourStart1, minStart1)
        flag2 = (hourEnd1, minEnd1) > (hourEnd2, minEnd2) > (hourStart1, minStart1)

        return flag1 or flag2


if __name__ == '__main__':
    main()
