import csv

# Collect average stats for each file run
def averageStats(filename, type):
    with open(filename, 'r') as file:
        lines = file.readlines()

    maxLine = len(lines)-1
    currentLine = 0

    csvName = type + '_stats.csv'

    # Open the CSV file in write mode
    with open(csvName, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['File', 'Lowest Optimal Cost', 'Number of Runs with the Lowest Optimal Cost', 'Average Time (seconds)', 'Average Number of Routes Explored'])

        # Search through each new file tested
        while currentLine <= maxLine:
            line = lines[currentLine]

            # End of this file output
            linesLeft = lines[currentLine:]
            fileStopper = linesLeft.index('--------------------------------------------------\n')

            # Get the filename
            startIndex = line.rfind('/') + 1
            endIndex = line.rfind('.')
            filename = line[startIndex:endIndex]

            # Average stats to collect
            lowestOptimalCost = float('inf') # Lowest optimal cost found
            sameLowestAnswer = 0 # Number of times this lowest optimal cost was found out of 30 runs 
            totalTime = 0 # Later converted to average
            totalOptionsExplored = 0 # Later converted to average

            # Get info from first run of a particular file = default values
            firstRunDetails = lines[currentLine:currentLine+fileStopper]

            for line in firstRunDetails:
                if "Optimal cost" in line:
                    lowestOptimalCost = int(line.split()[-1])
                    sameLowestAnswer += 1
                elif "Time taken" in line:
                    totalTime += float(line.split()[-2])
                elif "Options explored" in line:
                    totalOptionsExplored += int(line.split()[-1])

            runNumber = 1

            # Calculate for all runs of this file instance
            while runNumber < 30:
                currentLine += (fileStopper+1)

                line = lines[currentLine]

                # End of this file output
                linesLeft = lines[currentLine:]
                fileStopper = linesLeft.index('--------------------------------------------------\n')

                # Get info from first run of a particular file = default values
                runDetails = lines[currentLine:currentLine+fileStopper]

                for line in runDetails:
                    if "Optimal cost" in line:
                        value = int(line.split()[-1])

                        if value < lowestOptimalCost:
                            lowestOptimalCost = value
                            sameLowestAnswer = 1
                        elif value == lowestOptimalCost:
                            sameLowestAnswer += 1
                    elif "Time taken" in line:
                        totalTime += float(line.split()[-2])
                    elif "Options explored" in line:
                        totalOptionsExplored += int(line.split()[-1])

                runNumber += 1

            # Calculate averages
            averageTime = round(totalTime / 30, 6) # Rounded to 6 decimal places
            averageOptions = int(totalOptionsExplored / 30) # Truncated to integer

            print(filename)
            print(averageTime)
            print(averageOptions)
            print(lowestOptimalCost)
            print(sameLowestAnswer)
            print('---')

            # Write the data row
            writer.writerow([filename, lowestOptimalCost, sameLowestAnswer, averageTime, averageOptions])

            currentLine += (fileStopper+1)
        


averageStats('output_bnb.txt', 'B&B')