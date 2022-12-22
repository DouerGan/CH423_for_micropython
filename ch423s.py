from machine import Pin,SoftI2C,I2C
class CH423S:
    def __init__(self,i2c:SoftI2C,odOutPutMode=False,inputIoOutPutmode=False):
        self.odOutPutMode=odOutPutMode
        self.inputIoOutPutmode=inputIoOutPutmode
        self.i2c=i2c
        self.WriteData(0x48,(0b0|(self.odOutPutMode<<4))|self.inputIoOutPutmode)
        self.iopin0_7=[1]*8
        self.oc1pin0_7=[1]*8
        self.oc2pin0_7=[1]*8

        if self.inputIoOutPutmode:
            self.WriteData(0x60,self.ListToBin(self.iopin0_7))
        self.WriteData(0x44,self.ListToBin(self.oc1pin0_7))
        self.WriteData(0x46,self.ListToBin(self.oc2pin0_7))


    def SetValue(self,iogroup:int,Pin:int,value:int):
        if not 1<=iogroup<=3:
            raise Exception("The iogroup is incorrect,please use group 1-3")
        if not 0<=Pin<=7:
                raise Exception("The pin number is incorrect,please use pin 0-7")
        if value not in [0,1]:
                raise Exception("The pin value is incorrect,please use 0 or 1")
        if iogroup==1:
            if not self.inputIoOutPutmode:
                raise Exception("inputIoOutPutmode must be 1(True)")
            else:
                self.iopin0_7[Pin]=value
                self.WriteData(0x60,self.ListToBin(self.iopin0_7))
        elif iogroup==2:
            self.oc1pin0_7[Pin]=value
            self.WriteData(0x44,self.ListToBin(self.oc1pin0_7))
        else:
            self.oc2pin0_7[Pin]=value
            self.WriteData(0x46,self.ListToBin(self.oc2pin0_7))
    def ReadValue(self,iogroup:int,Pin:int):
        if not 1<=iogroup<=3:
            raise Exception("The iogroup is incorrect,please use group 1-3")
        if not 0<=Pin<=7:
                raise Exception("The pin number is incorrect,please use pin 0-7")
        if iogroup==2:
            return self.oc1pin0_7[Pin]
        elif iogroup==3:
            return self.oc2pin0_7[Pin]
        elif self.inputIoOutPutmode:
            return self.iopin0_7[Pin]
        else:
            return(self.BinToList(self.ReadData(0x4d)))[Pin]

    def Update(self):
        if not self.inputIoOutPutmode:
            self.WriteData(0x60,self.ListToBin(self.iopin0_7))
        self.WriteData(0x44,self.ListToBin(self.oc1pin0_7))
        self.WriteData(0x46,self.ListToBin(self.oc2pin0_7))

    def WriteData(self,cmd:int,data:int):
        self.i2c.start()
        self.i2c.write(bytearray([cmd,data]))
        self.i2c.stop()

    def ReadData(self,cmd:int):
        data=bytearray(1)
        self.i2c.start()
        self.i2c.write(bytearray([cmd]))
        self.i2c.readinto(data)
        self.i2c.stop()
        return data

    def ListToBin(self,l:list):
        a=''
        for i in l:
            a=str(i)+a
        return int(a,2)

    def BinToList(self,value:bytearray):
        b=value
        tt=7
        ll=[b[0]&1]
        while tt!=-0:
            b[0]>>=1
            ll.append(b[0]&1)
            tt-=1
        return ll

# from machine import Pin,SoftI2C,I2C
# from struct import pack
# pinEN=Pin(16,Pin.OUT,value=1)
# intIo35=Pin(35)
# i2cmux=Pin(14,Pin.OUT,value=1)
# i2c=SoftI2C(scl=Pin(33),sda=Pin(32),freq=400000)
# c=CH423S(i2c,0,1)
# c.setIO(iogroup=1,Pin=1,value=1)
# c.setIO(2,4,3)

