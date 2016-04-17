from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import operator
import logging
import functools
import time
import struct

logger = logging.getLogger(__name__)

from ..abstract import AbstractListener
from ...formats import km


class Sis(AbstractListener):
    """Konsberg SIS listener"""

    def __init__(self, port, datagrams, timeout=1, ip="0.0.0.0", target=None, name="Km"):
        super(Sis, self).__init__(port=port, datagrams=datagrams, ip=ip, timeout=timeout,
                                  target=target, name=name)
        self.desc = "Kongsberg SIS"

        # A few Nones to accommodate the potential types of datagrams that are currently supported
        self.id = None
        self.surface_ssp = None
        self.nav = None
        self.installation = None
        self.runtime = None
        self.ssp = None
        self.svp_input = None
        self.xyz88 = None
        self.range_angle78 = None
        self.seabed_image89 = None
        self.watercolumn = None
        self.bist = None

    def __repr__(self):
        msg = "%s" % super(Sis, self).__repr__()
        # msg += "  <has data loaded: %s>\n" % self.has_data_loaded
        return msg

    @classmethod
    def request_iur(cls, ip, port=4001):
        # Leaving this statement on until I have a chance to test with all systems.
        logger.info("Requesting profile from %s:%s" % (ip, port))

        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # We try all of them in the hopes that one works.
        sensors = ["710", "122", "302", "3020", "2040"]
        for sensor in sensors:

            # talker ID, Roger Davis (HMRG) suggested SM based on something KM told him
            output = '$SMR20,EMX=%s,' % sensor

            # calculate checksum, XOR of all bytes after the $
            checksum = functools.reduce(operator.xor, map(ord, output[1:len(output)]))

            # append the checksum and end of datagram identifier
            output += "*{0:02x}".format(checksum)
            output += "\\\r\n"

            sock_out.sendto(output.encode('utf-8'), (ip, port))

            # Adding a bit of a pause
            time.sleep(0.5)

        sock_out.close()

    def parse(self):
        this_data = self.data[:]

        self.id = struct.unpack("<BB", this_data[0:2])[1]

        try:
            name = km.Km.datagrams[self.id]
        except KeyError:
            name = "Unknown name"

        logger.info("%s > DG %d/0x%x/%c [%s] > sz: %.2f KB"
                    % (self.sender, self.id, self.id, self.id, name, len(this_data)/1024))

        if not (self.id in self.datagrams):
            return

        if self.id == 0x42:
            self.bist = km.KmBist(this_data)

        elif self.id == 0x47:
            self.surface_ssp = km.KmSsp(this_data)

        elif self.id == 0x49:
            self.installation = km.KmInstallation(this_data)

        elif self.id == 0x4e:
            self.range_angle78 = km.KmRangeAngle78(this_data)

        elif self.id == 0x50:
            self.nav = km.KmNav(this_data)

        elif self.id == 0x52:
            self.runtime = km.KmRuntime(this_data)

        elif self.id == 0x55:
            self.ssp = km.KmSvp(this_data)

        elif self.id == 0x57:
            self.svp_input = km.KmSvpInput(this_data)

        elif self.id == 0x58:
            self.xyz88 = km.KmXyz88(this_data)

        elif self.id == 0x59:
            self.seabed_image89 = km.KmSeabedImage89(this_data)

        elif self.id == 0x6b:
            self.watercolumn = km.KmWatercolumn(this_data)

        else:
            logger.error("Missing parser for datagram type: %s" % self.id)

    def dump_to_file(self):
        """Overloaded function to write data as Kongsberg .all format."""

        # Writing the length of each datagram as a 4-byte unsigned integer before the datagram.
        l = struct.pack("<I", len(self.data))  # hard-wired for little-endian byte-ordering
        self.raw_file.write(l)

        self.raw_file.write(self.data)