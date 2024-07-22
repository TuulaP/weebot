

import sys
import xml.etree.ElementTree as ET
#import datetime as dt
from datetime import datetime as dtime, timezone, timedelta

from fmiopendata.wfs import download_stored_query
from owslib.wfs import WebFeatureService
from math import isnan


# https://www.ilmatieteenlaitos.fi/tallennetut-kyselyt 

wfsserver = "https://opendata.fmi.fi/wfs"
wfs = WebFeatureService(url=wfsserver, version='2.0.0')

#print(wfs.identification.title)



def getFmiData (place="Kustavi Isokari"):

    # Retrieve the latest hour of data from a bounding box

    # 3.11 dtime.utcnow() #
    # 3.12 dtime.now(timezone.utc) # 
    end_time =  dtime.utcnow()
    # new format: 2024-07-17T16:08:42 00:00Z'
    #             2024-07-17 16:10:17.783129
    #print(end_time)
    #  # new: dt.datetime.now(dt.UTC) ?
    start_time = end_time - timedelta(hours=1)

    # Convert times to properly formatted strings

    start_time = start_time.isoformat(timespec="seconds") + "Z"

    # -> 2020-07-07T12:00:00Z

    end_time = end_time.isoformat(timespec="seconds") + "Z"

    # -> 2020-07-07T13:00:00Z

    # "bbox separated with commas as a value. 
    # The first two numbers express the lower left corner and 
    # the last two the top right corner coordinates of the bounding box
    # "bbox=18,55,35,75"

    #Helsinki,Mikkeli,Jyväskylä
    #place={0}&place=Helsinki -> quick fix for multiple places
    multiloc = place.replace(",","&place=")
    

    obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["starttime=" + start_time,
                                  "endtime=" + end_time,
                                  "place={0}".format(multiloc),
                                  #"place={0}".format(place),
                                    ])



    latest_tstep = max(obs.data.keys())
     

    ##print("voop", obs.data[latest_tstep].keys())

    # place name might be diff  from measurement place name
    # for now 1st is enough
    measplacename = next(iter(obs.data[latest_tstep].keys()))
    

    #print(sorted(obs.data[latest_tstep][measplacename].keys()))
    # -> ['Air temperature',
#     'Cloud amount',
#     'Dew-point temperature',
#     'Gust speed',
#     'Horizontal visibility',
#     'Precipitation amount',
#     'Precipitation intensity',
#     'Present weather (auto)',
#     'Pressure (msl)',
#     'Relative humidity',
#     'Snow depth',
#     'Wind direction',
#     'Wind speed']


#    print(obs.data[latest_tstep][measplacename]["Air temperature"])
#    print(obs.data[latest_tstep][measplacename]["Present weather (auto)"]) # 62?81?
#    print(obs.data[latest_tstep][measplacename]["Precipitation intensity"])
#    print(obs.data[latest_tstep][measplacename]["Snow depth"])
    res= {}

    for measplacename in obs.data[latest_tstep].keys():
        res[measplacename]=(measplacename.split(" ")[0],latest_tstep,
        obs.data[latest_tstep][measplacename]["Air temperature"],
        obs.data[latest_tstep][measplacename]["Precipitation amount"],
        obs.data[latest_tstep][measplacename]["Snow depth"])


    #print("Tul",res)
    
    return res
    # if "," in place:
    #     return res
    # else:
    #     return (latest_tstep,
    #     obs.data[latest_tstep][measplacename]["Air temperature"],
    #     obs.data[latest_tstep][measplacename]["Precipitation amount"],
    #     obs.data[latest_tstep][measplacename]["Snow depth"]
    #     )




def getFmiDataOLD(place):


    #sq = [storedquery.id for storedquery in wfs.storedqueries]
    #print(sq)
    #params = [parameter.name for parameter in wfs.storedqueries[1].parameters]
    #print(params)

    xmlbyteresponse = wfs.getfeature(storedQueryID='fmi::observations::weather::timevaluepair', storedQueryParams={'ID':'obs-obs-1-1-t2m','place':place,'timestep':'30'})

    response = xmlbyteresponse
    txtresp = ""
    wfsfile = "demo.xml"


    # converting the response to text
    for d in response:
        txtresp += d.decode()


    # temp xml for debugging & processing

    with open(wfsfile,"w") as filex:
        print(txtresp, file = filex)



    # parse thse result xml
    # There is probably some module for this, but couldn't find it... )

    xml_tree = ET.parse(wfsfile)  # fromstr returns root.

    root = xml_tree.getroot()

    latesttime = ""
    latesttemp = ""

    #  the hard way   
    for wfsmember in root:

        for omso in wfsmember:   #http://inspire.ec.europa.eu/schemas/omso/3.0}PointTimeSeriesObservation 

            #print(omso)
            for elem in omso:

                if elem.tag == "{http://www.opengis.net/om/2.0}result":
                    
                    for mts in elem:

                        #print("TAg2", mts.tag)
                        #print("K:",mts.keys())
                        #print("ATTR:", mts.attrib)
                        #print("ID: ", mts.attrib['id'])

                        if mts.attrib['{http://www.opengis.net/gml/3.2}id'] == "obs-obs-1-1-t2m": # atmosphere
                            for wmlpoint in mts:
                                for measu in wmlpoint:
                                    for mtvp in measu: 
                                        if mtvp.tag == "{http://www.opengis.net/waterml/2.0}time":
                                            latesttime = mtvp.text

                                        if (mtvp.tag == "{http://www.opengis.net/waterml/2.0}value" and mtvp.text != "NaN"):
                                            latesttemp = mtvp.text
    return (latesttime,latesttemp)



def fixEmptyRain (temp):
    units = temp['units']
    
    if isnan(temp['value']) or temp['value'] is None or temp['value']<0: # for snow/rain <0 is of no use
        res=0
    else:
        res = temp['value']

    return (res, units)



if __name__ == "__main__":

    place = ""


    if len(sys.argv) > 1:
        place = sys.argv[1]
    else:
        place = "Turku,Tornio"

    allres = getFmiData(place)

    restxt = ""

    for aplace in allres:
#       wtime, wtemp, wrain, wsnow = getFmiData(place)
        placen, wtime, wtemp, wrain, wsnow = allres[aplace]

        wrain,_ = fixEmptyRain(wrain)
        wsnow,_ = fixEmptyRain(wsnow)

        restxt += "Temp at {1} --> {0}C. Rain:{2} mm/h. ❄️:{3}".format(wtemp['value'],placen, wrain, wsnow) + "\n"



    #wtimef = dtime.datetime.now().astimezone().isoformat()
    wtimef = dtime.now().astimezone().isoformat()

    restxt = "Sää {0}\n".format(wtimef)+ restxt

    print(restxt)
    print("The end")



#Data <owslib.feature.wfs200.StoredQuery object at 0x0000015CBE23FEC0>
#starttime
#endtime
#timestep
#parameters
#crs
#bbox
#place
#fmisid
#maxlocations
#geoid
#wmo
# query = "fmi::observations::weather::simple"
# data = ""
# cou =0
# for spot in wfs.storedqueries:
#     if spot.id == query:
#         data = spot # wfs.storedqueries[query]
#         print("Foundit: ", query)
#         break
#     else : 

#         print(".", end="")


#     cou+=1

