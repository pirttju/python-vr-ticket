from bitstring import BitStream
import datetime

"""
Parser for the Small Structured Barcode (SSB)
used on RCT2 (Rail Combined Ticket 2) documents
defined in ERA TAP TSI technical document B.6.
Data is read from a 6-layer Aztec 2D barcode
as specified in UIC 918-2.
"""


class SSBData:
    # Strings are encoded using six-bit character codes
    _symbols = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
        16: "G",
        17: "H",
        18: "I",
        19: "J",
        20: "K",
        21: "L",
        22: "M",
        23: "N",
        24: "O",
        25: "P",
        26: "Q",
        27: "R",
        28: "S",
        29: "T",
        30: "U",
        31: "V",
        32: "W",
        33: "X",
        34: "Y",
        35: "Z",
    }

    _ticket_types = {1: "IV", 2: "IR", 3: "BP", 4: "IQ", 5: "IM", 6: "IO", 7: "IP", 8: "IK", 9: "IT"}

    # Translation from 6-bit to alphanumerical
    def _translate(self, data):
        out = []
        for num in data:
            out.append(self._symbols.get(num, " "))
        return "".join(out)

    # Translation of a timeslot number
    # 48 slots of 30 minutes:
    # 00:00 to 00:29: timeslot 1
    # 00:30 to 00:59: timeslot 2
    # ...
    def _timeslot(self, num):
        if num == 0:
            return ""
        else:
            zero = datetime.datetime(100, 1, 1, 0, 0, 0)
            slot_start = zero + datetime.timedelta(minutes=(num - 1) * 30)
            slot_end = zero + datetime.timedelta(minutes=(num - 1) * 30 + 29)
            return slot_start.strftime("%H:%M") + "-" + slot_end.strftime("%H:%M")

    # Translation of a ticket type
    def _ticket_type(self, num):
        return self._ticket_types.get(num, str(num))

    # Parser
    def __init__(self, data):
        s = BitStream(bytes=data)
        # Header - version number
        self.version = s.read("uint4")
        # Packet 177 - Issuing railway code
        self.issuing_railway = s.read("uint14")
        # Packet 242 - RCT2 type indicator
        # 1 = single segment
        # 2 = bi-segment
        self.rct2_type = 1 if s.read("uint1") == 0 else 2
        # Packet 200 - Number of ticket
        # blank or total number of tickets (always blank, not used by VR?)
        # TODO: implement the translation algorithm if necessary
        self.number_of_ticket = s.read("pad6")
        # Packet 137 - Number of adult passengers
        self.adult_passengers = s.read("uint7")
        # Packet 138 - Number of child passengers
        self.children_passengers = s.read("uint7")
        # Packet 142 - First day of validity
        self.valid_from = s.read("uint9")
        # Packet 143 - Last day of validity
        self.valid_to = s.read("uint9")
        # Packet 243 - "Corporate" frequent, or
        # Packet 171 - "Individual" frequent
        p_171 = s.read("uint1")
        self.corporate_frequent = p_171 == 0
        self.individual_frequent = p_171 == 1
        self.customer_number = s.read("uint47")
        # Packet 145 - Departure station
        p_145_an = s.read("uint1")
        if p_145_an == 0:
            p_145_bs = s.readlist("5*uint6")
            p_145 = self._translate(p_145_bs)
        else:
            p_145 = s.read("uint20")
            s.read("pad10")
        self.departure_station = p_145
        # Packet 146 - Arrival station
        p_146_an = s.read("uint1")
        if p_146_an == 0:
            p_146_bs = s.readlist("5*uint6")
            p_146 = self._translate(p_146_bs)
        else:
            p_146 = s.read("uint20")
            s.read("pad10")
        self.arrival_station = p_146
        # Packet 148 - Departure time
        # Translated into 48 slots of 30 minutes
        p_148 = s.read("uint6")
        self.departure_time = self._timeslot(p_148)
        # Packet 149 - Train number
        self.train_number = s.read("uint17")
        # Packet 206 - Reservation reference
        self.reservation_reference = s.read("uint40")
        # Packet 215 - Class of transport
        p_215 = s.readlist("1*uint6")
        self.class_of_transport = self._translate(p_215)
        # Packet 151 - Coach number
        self.coach_number = s.read("uint10")
        # Packet 153 - Seat / berth number
        # 00..99 + char
        p_153_num = s.read("uint7")
        p_153_bs = s.readlist("1*uint6")
        p_153_char = self._translate(p_153_bs)
        self.seat_number = str(p_153_num).zfill(2) + p_153_char
        # Packet 154 - Overbooking indicator
        self.overbooking = s.read("bool")
        # Packet 219 - Issuer's Passenger Name Record (PNR)
        p_219 = s.readlist("7*uint6")
        self.pnr_number = self._translate(p_219)
        # Packet 196 - Ticket type
        p_196 = s.read("uint4")
        self.ticket_type = self._ticket_type(p_196)
        # Packet 198 - "Specimen" code
        # 0 = test ticket
        # 1 = operational ticket
        self.specimen_code = s.read("uint1")
        # Via Stations (5 records)
        via = s.readlist("5*uint6")
        self.via_stations = self._translate(via)
        # Hash Code (CRC-32)
        self.hash_code = s.read("hex32")
        # Digital Seal
        self.digital_seal = s.read("hex480")
