import csv

# Collect average stats for each file run
def averageStats(filename, type):
    with open(filename, 'r') as file:
        lines = file.readlines()

    maxLine = len(lines) - 1
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
            try:
                fileStopper = linesLeft.index('--------------------------------------------------\n')
            except ValueError:
                break

            # Get the filename
            startIndex = line.rfind('/') + 1
            endIndex = line.rfind('.')
            filename = line[startIndex:endIndex]

            # Average stats to collect
            lowestOptimalCost = float('inf')  # Lowest optimal cost found
            sameLowestAnswer = 0  # Number of times this lowest optimal cost was found out of 30 runs
            totalTime = 0  # Later converted to average

            # Check if error occurred in the first run
            firstRunDetails = lines[currentLine:currentLine + fileStopper]
            memoryError = False
            timeoutError = False
            sizeError = False
            for line in firstRunDetails:
                if "Error:" in line:
                    if "Killed" in line:
                        memoryError = True
                        break
                    elif "timeout" in line:
                        timeoutError = True
                        break
                    elif "Traceback" in line:
                        sizeError = True
                        break
                elif "Optimal cost" in line:
                    lowestOptimalCost = float(line.split()[-1])
                    sameLowestAnswer += 1
                elif "Time taken" in line:
                    totalTime += float(line.split()[-2])

            if memoryError:
                writer.writerow([filename, "Out of Memory", "Out of Memory", "Out of Memory"])
                for _ in range(3):
                    currentLine += (fileStopper + 1)
                    linesLeft = lines[currentLine:]
                    if linesLeft:
                        try:
                            fileStopper = linesLeft.index('--------------------------------------------------\n')
                        except ValueError:
                            break
                    else:
                        break
                continue

            if timeoutError:
                writer.writerow([filename, "Timeout", "Timeout", "Timeout"])
                currentLine += (fileStopper + 1)
                linesLeft = lines[currentLine:]
                if linesLeft:
                    try:
                        fileStopper = linesLeft.index('--------------------------------------------------\n')
                    except ValueError:
                        break
                else:
                    break
                continue

            if sizeError:
                writer.writerow([filename, "Qubit Limit", "Qubit Limit", "Qubit Limit"])
                for _ in range(3):
                    currentLine += (fileStopper + 1)
                    linesLeft = lines[currentLine:]
                    if linesLeft:
                        try:
                            fileStopper = linesLeft.index('--------------------------------------------------\n')
                        except ValueError:
                            break
                    else:
                        break
                continue

            runNumber = 1

            # Calculate for all runs of this file instance
            while runNumber < 3:
                currentLine += (fileStopper + 1)
                line = lines[currentLine]

                # End of this file output
                linesLeft = lines[currentLine:]
                try:
                    fileStopper = linesLeft.index('--------------------------------------------------\n')
                except ValueError:
                    break

                # Get info from subsequent runs of the same file
                runDetails = lines[currentLine:currentLine + fileStopper]
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
            averageTime = round(totalTime / 3, 6)  # Rounded to 6 decimal places

            # Write the data row
            writer.writerow([filename, lowestOptimalCost, sameLowestAnswer, averageTime])

            print("Written")

            currentLine += (fileStopper + 1)

# Classical
averageStats('output_bnb.txt', 'B&B')
averageStats('output_sa.txt', 'SA')

# Quantum
averageStats('output_qaoa_coblya_5.txt', 'QAOA_COBLYA_5')
averageStats('output_qaoa_spsa_5.txt', 'QAOA_SPSA_5')

averageStats('output_vqe_coblya_RA.txt', 'VQE_COBLYA_RA')
averageStats('output_vqe_spsa_RA.txt', 'VQE_SPSA_RA')