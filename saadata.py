
import sys
import xml.etree.ElementTree as ET


from owslib.wfs import WebFeatureService

# https://www.ilmatieteenlaitos.fi/tallennetut-kyselyt 
wfsserver = "https://opendata.fmi.fi/wfs"
wfs = WebFeatureService(url=wfsserver, version='2.0.0')
#print(wfs.identification.title)


def getFmiData(place):

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


    # parse the result xml
    # There is probably some module for this, but couldn't find it... )
    xml_tree = ET.parse(wfsfile)  # fromstr returns root.
    root = xml_tree.getroot()

    latesttime = ""
    latesttemp = ""


    # This is horrid, but couldn't find suitable example from docs, sry :)

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



if __name__ == "__main__":

    place = ""

    if len(sys.argv) > 1:
        place = sys.argv[1]
    else:
        place = "Turku"

    wtime, wtemp = getFmiData(place)

    print("Temp at {2} on {0} --> {1}C".format(wtime,wtemp,place))


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
