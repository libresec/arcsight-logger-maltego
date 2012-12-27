aslMaltego
==========
ArcSight Logger / Maltego Integration

aslMaltego.py 
----------------
Module that handles communications with ArcSight logger, including authentication, 
SOAP clients, and error handling.

aslMaltego.conf
----------------
Configuration that holds ArcSight Logger username, password, and server information.
NOTE - The logger API only seems to work with local authentication.

Transforms
--------------------
maltego.IPv4Address (Entity)

	aslFireEye.py

FireEyeMalwareEvent.mtz
--------------------
Export of custom entity returned by aslFireEye.py transform.

Dependencies 
-------------
These transforms have been tested in Mac OSX using Python 2.7. In addition, SUDS is used 
SOAP-related needs.

Thanks
-----------------
Paterva (@Paterva)<br/>
@bostonlink<br/>
@ph1lv -- Thanks for the ideas!
