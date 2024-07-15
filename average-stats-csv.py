import csv

# Collect average stats for each quantum file run
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
        writer.writerow(['File', 'Lowest Optimal Cost', 'Number of Runs with the Lowest Optimal Cost', 'Average Time (seconds)'])

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

            # Get info from first run of a particular file = default values
            firstRunDetails = lines[currentLine:currentLine+fileStopper]

            for line in firstRunDetails:
                if "Optimal cost" in line:
                    lowestOptimalCost = float(line.split()[-1])
                    sameLowestAnswer += 1
                elif "Time taken" in line:
                    totalTime += float(line.split()[-2])

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
                        value = float(line.split()[-1])

                        if value < lowestOptimalCost:
                            lowestOptimalCost = value
                            sameLowestAnswer = 1
                        elif value == lowestOptimalCost:
                            sameLowestAnswer += 1
                    elif "Time taken" in line:
                        totalTime += float(line.split()[-2])

                runNumber += 1

            # Calculate averages
            averageTime = round(totalTime / 30, 6) # Rounded to 6 decimal places

            # Write the data row
            writer.writerow([filename, lowestOptimalCost, sameLowestAnswer, averageTime])

            print("Written")

            currentLine += (fileStopper+1)

# Classical
averageStats('output_bnb.txt', 'B&B')
averageStats('output_sa.txt', 'SA')

# Quantum
averageStats('output_qaoa_coblya_4.txt', 'QAOA_COBLYA_4')
averageStats('output_qaoa_coblya_10.txt', 'QAOA_COBLYA_10')
averageStats('output_qaoa_coblya_16.txt', 'QAOA_COBLYA_16')
averageStats('output_qaoa_spsa_4.txt', 'QAOA_SPSA_4')
averageStats('output_qaoa_spsa_10.txt', 'QAOA_SPSA_10')
averageStats('output_qaoa_spsa_16.txt', 'QAOA_SPSA_16')

averageStats('output_vqe_coblya_ES.txt', 'VQE_COBLYA_ES')
averageStats('output_vqe_coblya_RA.txt', 'VQE_COBLYA_RA')
averageStats('output_vqe_spsa_ES.txt', 'VQE_SPSA_ES')
averageStats('output_vqe_spsa_RA.txt', 'VQE_SPSA_RA')