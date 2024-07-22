
from botita import sendSimpleToot
from saadata import getFmiData, fixEmptyRain
import sys
from datetime import datetime as dtime, timezone, timedelta

# put this to scheduler or cron

if __name__ == "__main__":

    place = ""

    if len(sys.argv) > 1:
        place = sys.argv[1]
    else:
        place = "Turku,Heinola"

    restxt = ""

    allres = getFmiData(place)


    for aplace in allres:
#       wtime, wtemp, wrain, wsnow = getFmiData(place)
        placen, wtime, wtemp, wrain, wsnow = allres[aplace]

        wrain,_ = fixEmptyRain(wrain)
        wsnow,_ = fixEmptyRain(wsnow)

        restxt += "Temp at {1} --> {0}C. Rain:{2} mm/h. ❄️:{3}".format(wtemp['value'],placen, wrain, wsnow) + "\n"


    #wtimef = dtime.datetime.now().astimezone().isoformat()
    wtimef = dtime.now().astimezone().isoformat()

    restxt = "Sää {0}\n".format(wtimef)+ restxt

    #print(restxt)

    #wtext = "Sää>{2} : {1}C. Sade {3} mm/h. ❄️:{4}. Klo {0}".format(wtime,wtemp['value'],place, wrain, wsnow)

    sendSimpleToot(restxt)


    print("Done! Thank u, come again.")