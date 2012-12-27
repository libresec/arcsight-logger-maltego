import aslMaltego, sys

ip = sys.argv[1]

session, cookie, search = aslMaltego.getLoggerClient()
query = '''deviceProduct = "MPS" AND sourceAddress = %s | cef destinationAddress name''' %(ip) 
results = aslMaltego.loggerSearch(search, cookie, query)
aslMaltego.loggerLogout(session, cookie)

header="""<MaltegoMessage>
        <MaltegoTransformResponseMessage>
            <Entities>"""

footer="""        </Entities>
        </MaltegoTransformResponseMessage> 
    </MaltegoMessage>"""
    
print header

for result in results:
    print"""            <Entity Type='libresec.arcsightlogger.FireEyeMalwareEvent'>
                <Value>FireEye Event</Value>"""
    print"""                    <DisplayInformation>"""
    print"""                        <Label Name="Destination Address" Type="text/plain">%s</Label>""" %(result[-2])
    print"""                        <Label Name="Name" Type="text/plain">%s</Label>""" %(result[-1])
    print"""                    </DisplayInformation>"""
    print"""           </Entity>""" 

print footer