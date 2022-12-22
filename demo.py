from machine import Pin,I2C,SoftI2C,SPI,UART
from ch423s import CH423S
from machine import SoftI2C
simulativeI2cBus=SoftI2C(scl=Pin(33),sda=Pin(32),freq=400000)
ioExpansion=CH423S(i2c=simulativeI2cBus,odOutPutMode=False,inputIoOutPutmode=False)
#3个参数分别是
#       SoftI2c对象，
#       开漏输出是否（默认0关闭（推挽）），
#       双向IO（group_1）是否输出，默认输入（0）
ioExpansion.SetValue(iogroup=2,Pin=4,value=1)   #设置第二组IO,第4个IO，值为1
ioExpansion.ReadValue(iogroup=1,Pin=0)          #读取第一组IO,第0个IO的值
ioExpansion.Update()
'''
CH423SIO拓展IC可拓展24个GPIO,
其中8个双向IO
16个输出IO
分为3组，
第1组为8个双向IO，可通过inputIoOutPutmode参数设置输入或输出
第2,3组为输出IO，可通过odOutPutMode参数设置推挽或开漏输出
.SetValue()为设置输出IO的值
.ReadValue()为读取所有IO的值（输入和输出）
.Update()为更新输出IO值，最好定时更新防止干扰
'''
