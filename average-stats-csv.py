import csv
import numpy as np

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
        writer.writerow(['File', 'Lowest Optimal Cost', 'Number of Runs with the Lowest Optimal Cost', 'Highest Optimal Cost', 
                         'Number of Runs with the Highest Optimal Cost', 'Best Time (seconds)', 'Average Time (seconds)', 
                         'Worst Time (seconds)', 'Standard Deviation of Optimal Cost', 'Standard Deviation of Time'])

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
            optimalCosts = []  # List to store optimal costs
            times = []  # List to store times
            lowestOptimalCost = float('inf')  # Lowest optimal cost found
            highestOptimalCost = 0  # Highest optimal cost found
            sameLowestAnswer = 0  # Number of times this lowest optimal cost was found out of 30 runs
            sameHighestAnswer = 0  # Number of times this highest optimal cost was found out of 30 runs
            quickestTime = float('inf')  # Quickest time taken to find the optimal cost
            longestTime = 0  # Longest time taken to find the optimal cost
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
                    elif "Timeout" in line:
                        timeoutError = True
                        break
                    elif "timeout" in line:
                        timeoutError = True
                        break
                    elif "Traceback" in line:
                        sizeError = True
                        break
                elif "Optimal cost" in line:
                    cost = float(line.split()[-1])
                    optimalCosts.append(cost)
                    lowestOptimalCost = min(lowestOptimalCost, cost)
                    highestOptimalCost = max(highestOptimalCost, cost)
                    sameLowestAnswer += 1 if cost == lowestOptimalCost else 0
                    sameHighestAnswer += 1 if cost == highestOptimalCost else 0
                elif "Time taken" in line:
                    time = float(line.split()[-2])
                    times.append(time)
                    totalTime += time

                    quickestTime = min(quickestTime, time)
                    longestTime = max(longestTime, time)

            if memoryError:
                writer.writerow([filename, "OOM", "OOM", "OOM", "OOM", "OOM", "OOM", "OOM", "OOM", "OOM"])
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
                writer.writerow([filename, "T", "T", "T", "T", "T", "T", "T", "T", "T"])
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
                writer.writerow([filename, "QL", "QL", "QL", "QL", "QL", "QL", "QL", "QL", "QL"])
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
                        optimalCosts.append(value)
                        if value < lowestOptimalCost:
                            lowestOptimalCost = value
                            sameLowestAnswer = 1
                        elif value == lowestOptimalCost:
                            sameLowestAnswer += 1
                        elif value > highestOptimalCost:
                            highestOptimalCost = value
                            sameHighestAnswer = 1
                        elif value == highestOptimalCost:
                            sameHighestAnswer += 1
                    elif "Time taken" in line:
                        time = float(line.split()[-2])
                        times.append(time)
                        totalTime += time

                        if time < quickestTime:
                            quickestTime = time
                        if time > longestTime:
                            longestTime = time

                runNumber += 1

            # Calculate averages and standard deviations
            # *************************** CHANGE TO 6 WHEN UPDATED RUNS ***************************
            averageTime = round(totalTime / 3, 6)  # Rounded to 6 decimal places
            stdDevOptimalCost = round(np.std(optimalCosts), 6)  # Standard deviation of optimal cost
            stdDevTime = round(np.std(times), 6)  # Standard deviation of time
            bestTime = round(quickestTime, 6)
            worstTime = round(longestTime, 6)

            # Write the data row
            writer.writerow([filename, lowestOptimalCost, sameLowestAnswer, highestOptimalCost, sameHighestAnswer,
                             bestTime, averageTime, worstTime, stdDevOptimalCost, stdDevTime])

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
