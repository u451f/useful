#!/usr/bin/env python
from stem.control import Controller

with Controller.from_port(port=9051) as xcontroller:
    xcontroller.authenticate()  # provide the password here if you set one
    BYTES_READ = xcontroller.get_info("traffic/read")
    BYTES_WRITTEN = xcontroller.get_info("traffic/written")
    print ("My Tor relay has read %s bytes and written %s." % (BYTES_READ, BYTES_WRITTEN))
