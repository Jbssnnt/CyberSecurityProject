import csv

def csvWrite(outputData, filename):
    """
    A simple function to write data to a
    csv file.

    Args:
        outputData: The data to be written.
            A list of lists.
        filename: A string with the name of
            the file to write to.

    Returns:
        Nothing
    """
    with open(filename, "w") as csvFile:
        writer = csv.writer(csvFile)
        for data in outputData:
            writer.writerow(data)
        csvFile.close()

def readPIDList(filename):
    """
    Simple function to read the list of PIDs to
    run the program on. Currently unused but may
    be added since PID's need to be read more than
    once.

    Args:
        filename: A string holding the filename
        to read from

    Returns:
        A dictionary of digits representing the PIDs
        to trace.
    """
    pidDictionary = {}
    with open(filename, 'r') as fileobj:
        lines = fileobj.readlines()

        for line in lines:
            words = line.split()
            if words[1].isdigit() and words[2].isdigit():
                pidDictionary[words[1]] = words[2]

        fileobj.close()

    return(pidDictionary)
