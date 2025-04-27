import csv
import sys

def main():
    #set up control variables
    prevDate = ""
    run = -1
    runVals = []
    for i in range(30): #data is not useful beyond 30 runs
        runVals.append([])
    csvrows = []
    #loop over each row, comparing date to previous
    with open(sys.argv[1], "r", encoding='utf-8') as data:
        #skip the first three rows
        for i in range(3):
            data.readline()
        #read each row into a list so we can easily index backwards
        for line in data.readlines():
            csvrows.append(line.split(","))

    #parse the rows in backwards order
    for i in range(len(csvrows)):
        position = (-1 - i)
        currentDate = csvrows[position][0][:-9]
        #if we detect a new date, set the first run of the day
        if currentDate != prevDate:
            prevDate = currentDate
            run = 0
        #ignore runs after the 30th of the day
        if run >= 30:
            pass
        #parse the time into seconds
        #igt is position 15
        try:
            timeFormatted = csvrows[position][15]
        except IndexError: #some rows are malformed - broken tracking
            pass
        #hours + mins + secs
        try:
            timeSeconds = (60 * 60 * int(timeFormatted[:1])) + (60 * int(timeFormatted[2:4]) + int(timeFormatted[5:]))
            runVals[run].append(timeSeconds)
        except ValueError: #thrown for runs with unmarked times
            pass
        #control
        run += 1

    #calculate avg and print
    for i in range(len(runVals)):
        try:
            avgSeconds = sum(runVals[i])/len(runVals[i])
        except ZeroDivisionError:
            #this skips printing rows with no data
            continue
        #divide out mins
        mins = int(avgSeconds / 60)
        secs = int(avgSeconds % 60)
        hours = 0
        #divide out hours if needed
        if mins > 59:
            hours = int(mins / 60)
            mins = mins % 60
        #print out average
        print("Average for run %d: %d:%02d:%02d" % ((i + 1), hours, mins, secs))



    

        

        

if __name__ == "__main__":
    main()