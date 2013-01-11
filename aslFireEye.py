'''
@author: libresec
'''
import aslMaltego, sys, tkSimpleDialog
import Tkinter as tk

ip = sys.argv[1]  

root = tk.Tk()
root.geometry("0x0")    # make root "tiny"
root.overrideredirect(1) # get rid of the frame, border, etc.
time=tkSimpleDialog.askinteger('aslMaltego', "Enter timeframe in hours:", initialvalue=1, minvalue=1, maxvalue=168)

#easygui verison of prompt-->
#import easygui as eg
#time = eg.integerbox("Enter timeframe in hours:", "aslMaltego", 24, 1, 168)

session, cookie, search = aslMaltego.getLoggerClient()
query = '''deviceProduct = "MPS" AND sourceAddress = %s | cef destinationAddress name''' %(ip) 
results = aslMaltego.loggerSearch(search, cookie, query, time)
aslMaltego.loggerLogout(session, cookie)

if results:
    header="""<MaltegoMessage>
        <MaltegoTransformResponseMessage>
            <Entities>"""
    footer="""        </Entities>
        </MaltegoTransformResponseMessage> 
    </MaltegoMessage>"""
    
    print header

    for result in results:
        print"""            <Entity Type='libresec.arcsightlogger.FireEyeMalwareEvent'>
                    <Value>%s</Value>""" %(result[-1])
        print"""                    <DisplayInformation>"""
        print"""                        <Label Name="Destination Address" Type="text/plain">%s</Label>""" %(result[-2])
        print"""                        <Label Name="Name" Type="text/plain">%s</Label>""" %(result[-1])
        print"""                    </DisplayInformation>"""
        print"""           </Entity>""" 
    
    print footer
    
else:
    aslMaltego.errors(2)