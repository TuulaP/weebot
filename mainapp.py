
from botita import sendSimpleToot
from saadata import getFmiData, fixEmptyRain
import sys

# put this to scheduler or cron

if __name__ == "__main__":

    place = ""

    if len(sys.argv) > 1:
        place = sys.argv[1]
    else:
        place = "Turku"

    wtime, wtemp, wrain, wsnow = getFmiData(place)

    wrain,_ = fixEmptyRain(wrain)
    wsnow,_ = fixEmptyRain(wsnow)

    wtext = "Sää>{2} : {1}C. Sade {3} mm/h. ❄️:{4}. Klo {0}".format(wtime,wtemp['value'],place, wrain, wsnow)

    sendSimpleToot(wtext)


    print("Done! Thank u, come again.")