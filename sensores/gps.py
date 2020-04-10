import navio.util
import navio.ublox

class Gps:

    ubl = navio.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)

    def __init__(self):

        self.ubl.configure_poll_port()
        self.ubl.configure_poll(navio.ublox.CLASS_CFG, navio.ublox.MSG_CFG_USB)
        #ubl.configure_poll(navio.ublox.CLASS_MON, navio.ublox.MSG_MON_HW)

        self.ubl.configure_port(port=navio.ublox.PORT_SERIAL1, inMask=1, outMask=0)
        self.ubl.configure_port(port=navio.ublox.PORT_USB, inMask=1, outMask=1)
        self.ubl.configure_port(port=navio.ublox.PORT_SERIAL2, inMask=1, outMask=0)
        self.ubl.configure_poll_port()
        self.ubl.configure_poll_port(navio.ublox.PORT_SERIAL1)
        self.ubl.configure_poll_port(navio.ublox.PORT_SERIAL2)
        self.ubl.configure_poll_port(navio.ublox.PORT_USB)
        self.ubl.configure_solution_rate(rate_ms=1000)

        self.ubl.set_preferred_dynamic_model(None)
        self.ubl.set_preferred_usePPP(None)

        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSLLH, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_PVT, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_STATUS, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SOL, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELNED, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SVINFO, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELECEF, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSECEF, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_RAW, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SFRB, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SVSI, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_ALM, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_EPH, 1)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_TIMEGPS, 5)
        self.ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_CLOCK, 5)
        #ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_DGPS, 5)
        print("modulo inicializado")


    """devuelve una tupla con la latitud y la longitud en formato decimal"""
    def get_coords(self):
        msg = self.ubl.receive_message()
        while msg.name() != "NAV_POSLLH":
            msg = self.ubl.receive_message()
        arr = str(msg).split(",")[1:3] #guardamos lat y long

        longg = arr[0]
        longg = longg.split("=")
        longg = float (longg[1])

        lat = arr[1]
        lat = lat.split("=")
        lat = float (lat[1])

        return lat, longg

#import gps
#a = gps.Gps()
#print(a.get_coords())