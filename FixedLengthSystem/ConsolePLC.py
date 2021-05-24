
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import time

class siemens():
    def conPLC(IP):
        siemens = SiemensS7Net(SiemensPLCS.S300, IP)
        if siemens.ConnectServer().IsSuccess == True :
            PLC = siemens
        elif siemens.ConnectServer().IsSuccess == False :
            PLC = "connect failed"
        return PLC

    #以下是读取PLC数据的函数
    def printReadResult(result):
        if result.IsSuccess:
            print(result.Content)
        else:
            print("failed   " + result.Message)

    #以下是写PLC的程序
    def printWriteResult(result):
        if result.IsSuccess:
            print("success")
        else:
            print("falied  " + result.Message)
''' 测试
    if __name__ == "__main__":
        siemens = SiemensS7Net(SiemensPLCS.S300, "192.168.0.1")
        if siemens.ConnectServer().IsSuccess == False:
            print("connect falied")
        else:
            # bool read write test
            siemens.WriteBool("M80.6", True)
            printReadResult(siemens.ReadBool("M80.6"))

            # byte read write test
            siemens.WriteByte("M100", 58)
            printReadResult(siemens.ReadByte("M100"))

            # int16 read write test
            siemens.WriteInt16("M102", 12358)
            printReadResult(siemens.ReadInt16("M102"))

            # float read write test
            siemens.WriteFloat("M130", 123456)
            printReadResult(siemens.ReadFloat("M130"))

            #以下是读写DB块的操作
            #bool read write test
            siemens.WriteBool("DB2.38.0", True)
            printReadResult(siemens.ReadBool("DB2.38.0"))

            # int16 read write test
            siemens.WriteInt16("DB2.0", 12358)
            printReadResult(siemens.ReadInt16("DB2.0"))

            # float read write test
            siemens.WriteFloat("DB2.14.0", 123456)
            printReadResult(siemens.ReadFloat("DB2.14.0"))

            # int16 array read write test
            siemens.WriteInt16("DB2.2.0", [123, 456, 789, -1234])
            printReadResult(siemens.ReadInt16("DB2.2.0", 4))

             #这段是自己写着实验玩的
            num = 10
            while num<=100:
                num = num + 1
                time.sleep(2)
                # int16 read write test
                print("num="+str(num))
                siemens.WriteInt16("DB2.12.0", num)
                printReadResult(siemens.ReadInt16("DB2.12.0")) '''
