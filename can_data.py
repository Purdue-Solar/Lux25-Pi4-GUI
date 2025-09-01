class CanData:
    def __init__(self):
        #Variable Initialization
        self.canid = 0
        self.data_bytes = [] #(self.data_bytes).len = 8
        self.packSOC = 0
        self.motorVelocity = 0
        self.motorCurrent = 0

        self.AuxCondition = 0
        self.MainCurrentWarning = 0
        self.MainOverCurrentError = 0
        self.MainUnderVoltage = 0
        self.MainOverVoltage = 0
        self.AuxCurrentWarning = 0
        self.AuxOverCurrent = 0
        self.AuxUnderVoltage = 0
        self.AuxOverVoltage = 0

        #Byte 0
        self.AuxMask = 1 << 1
        self.MainCurrentWarningMask = 1 << 4
        self.MainOverCurrentMask = 1 << 5
        self.MainUnderVotlageMask = 1 << 6
        self.MainOverVoltageMask = 1 << 7

        #Byte 1
        self.AuxCurrentWarningMask = 1 << 0
        self.AuxOverCurrentMask = 1 << 1
        self.AuxUnderVoltageMask = 1 << 2
        self.AuxOverVoltageMask = 1 << 3

    def checkCase(self):
        match self.canid:
            case 0x200:
                self.packSOC = self.rotateBits(self.data_bytes[4])
                print("Updated packSOC")
            case 0x402:
                self.motorCurrent = int(self.data_bytes[4] | (self.data_bytes[5] << 8) | (self.data_bytes[6] << 16) | (self.data_bytes[7] << (8*3)))
                print("Updated Motor Current")
            case 0x403:
                self.motorVelocity = int(self.data_bytes[4] | (self.data_bytes[5] << 8) | (self.data_bytes[6] << 16) | (self.data_bytes[7] << (8*3))) * 2.237 #m/s to mph
                print("Updated Motor Velocity")
            case 0x110040FF:
                #Byte 0
                self.AuxCondition         = (self.data_bytes[0] & self.AuxMask) >> 1
                self.MainCurrentWarning   = (self.data_bytes[0] & self.MainCurrentWarningMask) >> 4
                self.MainOverCurrentError = (self.data_bytes[0] & self.MainOverCurrentMask) >> 5
                self.MainUnderVoltage     = (self.data_bytes[0] & self.MainUnderVotlageMask) >> 6
                self.MainOverVoltage      = (self.data_bytes[0] & self.MainOverVoltageMask) >> 7

                #Byte 1
                self.AuxCurrentWarning = (self.data_bytes[1] & self.AuxCurrentWarningMask)
                self.AuxOverCurrent    = (self.data_bytes[1] & self.AuxOverCurrentMask) >> 1
                self.AuxUnderVoltage   = (self.data_bytes[1] & self.AuxUnderVoltageMask) >> 2
                self.AuxOverVoltage    = (self.data_bytes[1] & self.AuxOverVoltageMask) >> 3
                print("Updated Monitor value")
            case _:
                pass

        print(f"SOC = {self.packSOC}")
        
    def updateCAN(self, id, bytes):
        self.canid = id
        self.data_bytes = bytes
        self.checkCase()
    
    def rotateBits(self, bytes):
        bit0 = (bytes & 0x01)
        bit1 = (bytes & 0x02) >> 1
        bit2 = (bytes & 0x04) >> 2
        bit3 = (bytes & 0x08) >> 3
        bit4 = (bytes & 0x10) >> 4
        bit5 = (bytes & 0x20) >> 5
        bit6 = (bytes & 0x40) >> 6
        bit7 = (bytes & 0x80) >> 7
        return (bit0 << 7) | (bit1 << 6) | (bit2 << 5) | (bit3 << 4) | (bit4 << 3) | (bit5 << 2) | (bit6 << 1) | bit7 
