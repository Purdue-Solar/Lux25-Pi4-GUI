class CanId:
    def __init__(self, canid):
        self.canid = canid
        self.destbitmask = 0x000000FF
        self.sourcebitmask = 0x0000FF00
        self.sourceID = self.canid & self.sourcebitmask
        self.destID = self.canid & self.destbitmask
    
    def destlookup(self, dest):
        dests = {
            0x0: "Mppts",
            0x10: "BMS",
            0x20: "Motor",
            0x30: "Display",
            0x40: "Distribution",
            0x50: "Peripherals",
            0x60: "Steering",
            0x70: "Telemetry",
            0x1F: "Generic",
            0xFF: "Multicast"
        }
        return dests.get(dest, hex(dest))

    def sourcelookup(self, source):
        sources = {
            0x0: "Mppts",
            0x10: "BMS",
            0x20: "Motor",
            0x30: "Display",
            0x40: "Distribution",
            0x50: "Peripherals",
            0x60: "Steering",
            0x70: "Telemetry",
            0x1F: "Generic",
            0xFF: "Multicast"
        }
        return sources.get(source, hex(source))

    def messageidlookup(self, message):
        messages = {
            0x0: "Heartbeat",
            0x10: "VoltageCurrent0",
            0x20: "VoltageCurrent1",
            0x30: "VoltageCurrent2",
            0x40: "VoltageCurrent3",
            0x02: "Error0",
            0x12: "Error1",
            0x22: "Error2",
            0x32: "Error3",
            0xF3: "Reset"
        }
        return messages.get(message, hex(message))

    def deviceidlookup(self, device):
        devices = {
            0x0: "Mppts",
            0x01: "BMS",
            0x02: "Motor",
            0x03: "Display",
            0x04: "Distribution",
            0x05: "Peripherals",
            0x06: "Steering",
            0x07: "Telemetry",
            0xF1: "Generic",
            0xFF: "Multicast"
        }
        return devices.get(device, hex(device))

    def prioritylookup(self, priority):
        priorities = {
            0x0: "Highest",
            0x01: "High",
            0x02: "Medium",
            0x03: "Low"
        }
        return priorities.get(priority, hex(priority))
    
    def identify(self):
        
        pass