
from botita import sendSimpleToot
from saadata import getFmiData
import sys

# put this to scheduler or cron

if __name__ == "__main__":

    place = ""

    if len(sys.argv) > 1:
        place = sys.argv[1]
    else:
        place = "Turku"

    wtime, wtemp = getFmiData(place)

    sendSimpleToot("Sää {0}, {1}C, ({2})".format(place,wtemp,wtime))

    print("Done! Thank u, come again.")