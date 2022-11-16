# IoetExercise

This is my solution for the programming exercise given by the company ioet, to apply for the position: Junior Software Developers and Interns.

## Solution Overview

I divided the big problem into little ones to solve one by one. Roughly as follows:
1. Opennig the input file and getting the data from it.
2. Treating the data: Divide each worker's **name** and **schedule**.
3. Comparing the days.
4. Comparing the hours.
5. Comparing the minutes.
6. Main function

Let's go througth each one (I'll try to do it briefly):

### Opennig the input file and getting the data from it.

Opening the input file and reading it in python is straigth foward. A additional step I took was delelting the '\n' character in every line with the .strip() method. This step returns a list with each line as an element.

To access (and edit if necessary) the name of the file, I created a variable (which should be a constant, but python does not have that kind of data type) naming it in all capital letters to follow the convention.
```python3
FILENAME = 'input.txt'
```

### Treating the data: Divide each worker's **name** and **schedule**

Now, iterating over the list we separate the data and put into a dictionary with two keys: 'name' and 'days&hours'. For example: 
```python3
data = {'name': worker, 'days&hours': workerSchedule.split(',') } 
#      {'name': 'RENE', 'days&hours': ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00, 'SU01:00-02:00']}
```

This dictionaries are then put into a list so we can iterate over them.

### Comparing the days

Having the data ready to be manipulated, we must determine the order in which we are going to compare the time parameters to create the corresponding algorithms. I believe the correct way to do it is to first compare days, then hours and finally minutes. To compare the days I think I came up with a fairly clever and efficient algorithm:

**Preconditions**
- Have a list of days:
```python3
DAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
```
This next code snippet is some code combine with pseudocode, it is not the end result.
```python3
def checkDayCoincidences(worker1, worker2):
    #Examples
    worker1 = {'name': 'RENE', 'days&hours': ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'S'01:00-'02:00']
    worker2 = {'name': 'ASTRID', 'days&hours': ['MO10:00-12:00', 'TH12:00-14:00', 'S'01:00'02:00']}

    # Build the string of names:
    coincidenceNames = worker1['name'] + '-' + worker2['name'] + ':' # --> RENE-ASTRID:

    # Compare days:
    # for i = 0, j = 0, i++, j++
    day1 = worker1['days&hours'][i][:2] --> 'MO'
    day2 = worker2['days&hours'][j][:2] --> 'MO'
    dayDistance = DAYS.indexof(day1) - DAYS.indexof(day2) # --> 0 - 0 = 0
    if dayDistance == 0:
        checkHours()
    elif dayDistance > 0:
        continue
    elif dayDistance < 0:
        break
```

First, the name combination of the workers we are iterating over is created. This will be important because it is the expected output of the program. Then, it iterates over each worker schedule that is inside the list that has 'days&hours' as a key, taking only the first two characters. 
The day indices are then extracted from the DAYS list and subtracted (first loop day index minus second loop day index) to calculate its distance. With this value we make a nested if that validates if the distance between the days is equal to zero, greater than zero or less than zero. If it is equal to zero, it means that they are the same day, so we proceed to check the hours.Here comes the interesting thing. The order of the days is used to see if it is missing to reach the corresponding day or if it has already passed.
For example, if I search for Thursday and the second day (the one of the list that we are iterating in the second loop) is Tuesday, the distance will be greater than zero, so it will go to the next element (day). On the other hand, if it is Friday, the distance will be negative, so the loop stops, since we already know that if I continue searching after Friday I will never find Thursday.


### Comparing the hours

These two last steps where the most challeging ones. To make things easier, I divided the time comparison into several cases. The 3 first cases need solely analysis and comparison on the hour part. They are the following:

**Assumptions** 
- It is safe to assume that they will work at least an half-hour.

**Preconditions**
- Have a list of hours:
```python3
HOURS = [x for x in range(24)]
```
- Hours come sorted by which hourDistances is bigger.

***Case 1.1:*** They started at the same time, there is always an overlap --> return True, e.g.:
```python3
hours1 = ['12:00', '14:00'] 
hourDistance1 = 2
hours2 = ['12:00', '12:30']
hourDistance2 = 0
return hours1[0] == hours2[0] ? True : checkOtherCases()
```
Last line is not python syntax, but it takes less space and it's as easy to understand.

***Case 1.2:*** They end at the same time, there is always an overlap --> return True, e.g.:
```python3
hours1 = ['13:16', '14:00'] 
hourDistance1 = 0
hours2 = ['13:15', '14:00']
hourDistance2 = 0
return hours1[1] == hours2[1] ? True : checkOtherCases()
```
For the next cases I needed some way to get the range of hours that were recieve as input, for example:
If this is the input: ['22:00', '02:00'] then I need this --> [22, 23, 0, 1, 2], so I developt an algorithm for that.
```python3
# Lets try taking the full range of hours:
def getInterval(hours, hourDistance):
    start = int(hours[0][:2])
    end = start + hourDistance
    interval = HOURS[start:end + 1]
    if(len(interval) < hourDistance):
        remaining = hourDistance - len(interval) + 1
        interval += HOURS[:remaining]
    return interval # --> [22, 23, 0, 1, 2]
```

The algorithm takes the start and end of the interval. Since in the HOURS list the numbers correspond exactly to their indices, I take advantage of that to create this list. In the case that the interval includes '00', the list produced will not be complete and will only go up to 23. The conditional resolves this by asking if the length of the interval is less than the distance between them. If this is true, these 2 numbers are subtracted to find out how many numbers are missing from 23. Using this number, the list of hours is delimited and added to the interval, producing the complete list. More information on this function is on the script. Creating this interval list also has the advantage to make the code more readable.

***Case 2:*** No hour overlap. Works Fine e.g.:
```python3
hours1 = ['22:00', '02:00']
hourDistance1 = 4
hours2 = ['12:00', '14:00']
hourDistance2 = 2

interval = getInterval(hours1, hourDistance1) # --> [22, 23, 0, 1, 2]
startHour = int(hours2[0][:2]) # --> 12
endHour = int(hours2[1][:2]) # --> 14

comparisonStart = int(hours2[0][:2]) in interval # --> False
comparisonEnd = int(hours2[1][:2]) in interval # --> False

if(comparisonStart or comparisonEnd): # --> False
    #Keep checking
else:
    return False
```

#### Overlaps are the biggest problem

***Case 3:*** Overlap. Both hours2 hours are inside hours1 inteval (not including the ends of the interval). Works fine. For this case I created 2 new flags which use the prefix strict. E.g.:
```python3
hours1 = ['10:00', '15:00']
hourDistance1 = 5
hours2 = ['12:00', '14:00']
hourDistance2 = 2

interval = getInterval(hours1, hourDistance1) # --> [10, 11, 12, 13, 14, 15]
strictInterval = interval[1:-1] # --> [11, 12, 13, 14]
startHour = int(hours2[0][:2]) # --> 12
endHour = int(hours2[1][:2]) # --> 14

# Both true, which mean there is a coincidence
strictComparisonStart = startHour in strictInterval # --> True
strictComparisonEnd = endHour in strictInterval # --> True

comparisonStart = startHour in interval
comparisonEnd = endHour in interval

if(strictComparisonStart and strictComparisonEnd): # --> True
    return True
#More code...
```
This wraps up the cases that analyze just the hours.

### Comparing the minutes

These next two cases need analysis on hour and minutes:

***Case 4:*** Overlap. One or both hours are the same in both lists.
```python3
hours1 = ['10:30', '13:30'] # --> hourDistance1 = 3
hours2 = ['10:00', '11:15'] # --> hourDistance2 = 1
```
***Case 5:*** Hour overlap, but no minute overlap. No coincidence --> return False
```python3
hours1 = ['10:30', '13:30'] # --> hourDistance1 = 3
hours2 = ['10:00', '10:15'] # --> hourDistance2 = 0
```
For this cases, I created a function, taking inspiration from: https://stackoverflow.com/questions/45656834/python-compare-date-strings-without-using-built-in-functions-or-libraries. This post made me realized that if I put the entry and exit times in tuples with this format: (hour, minute), then it was possible to compare the tuples with good results. This is the algorithm:
```python3
def checkMinutesCoincidences(hours1, hours2):
    hourStart1, minStart1 = map(int, hours1[0].split(':'))
    hourEnd1, minEnd1 = map(int, hours1[1].split(':'))

    hourStart2, minStart2 = map(int, hours2[0].split(':'))
    hourEnd2, minEnd2 = map(int, hours2[1].split(':'))
    
    if((hourStart1, minStart1) > (hourStart2, minStart2)):
        flag1 = (hourEnd2, minEnd2) > (hourStart1, minStart1) > (hourStart2, minStart2)
        flag2 = (hourEnd2, minEnd2) > (hourEnd1, minEnd1) > (hourStart2, minStart2)

        return flag1 or flag2

    else:
        flag1 = (hourEnd1, minEnd1) > (hourStart2, minStart2) > (hourStart1, minStart1)
        flag2 = (hourEnd1, minEnd1) > (hourEnd2, minEnd2) > (hourStart1, minStart1)

        return flag1 or flag2
```
The only downside that I didn't have time to solve is that if the function recieves an interval that includes '00:00', e.g.: ['23:00', '01:00'] then it fails to compare correctly.

### Main function

The main function is quite simple. It will iterate over the same list of dictionaries twice to compare worker and with worker. Here is an example of the list:
```python3
data_schedules = [worker1, worker2, worker3, worker4, worker5]
```

The objective is to compare the first worker with the rest, then the second with the rest except the first because that comparison was already executed, then the third with the fourth and the fifth and so on. This is achieved by manipulating the indices so that the second index is always one more than the first, and stopping the loop when the maximum index is reached.
```python3
for i in range(len(workers)):
        j = i + 1
        while(j < len(workers)):
            flag, coincidences, names = checkDaysCoincidences(data_schedules[i],data_schedules[j])
            if(flag):
                print(f'{names} {coincidences}')
            j += 1
```

Finally, 3 values are extracted from the **checkDaysCoincidences** function, which is a flag that indicates whether or not there was a coincidence, the number of coincidences and the names of the workers who had that coincidence in their schedule.

## How to Run
You are only require to have installed Python in a current version. My code is a simple script, so all you have to do is, in a terminal window search the directory where the script is and type on command line:

```
python exercise.py
```
