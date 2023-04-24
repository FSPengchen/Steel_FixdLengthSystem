import socket
import binascii
import time

def Helper(conn):
    # data = s1.recv(1024)
    data = conn.recv(1024)
    # print(data)
    # print('data:', data, type(data), len(data))
    weightdict = {}
    # print('原始数据', data)
    # pro_data = binascii.b2a_hex(data)
    # print('转换为十六进制', str(pro_data),type(pro_data),len(pro_data))
    # print(data)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '二流重量', data[4:10])
    with open('2233.txt', 'a+') as f:
        f.writelines(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '2传感器线程重量' + str(binascii.b2a_hex(data[4:10])) + '\n')
    print(data)
    if len(data) == 18:
        weight_2liu = int((data[4:10]))

        # print('SOH:',SOH,type(SOH))
        # print('data[:1]报文引导信息头01H:', data[:1], str(binascii.b2a_hex(data[:1])))

        # ADDR = int(binascii.b2a_hex(data[1:2]))
        # # print('ADDR:',ADDR,type(ADDR))
        # # print('data[1:2]本显示器地址41H:', data[1:2], str(binascii.b2a_hex(data[1:2])))
        #
        # STX = int(binascii.b2a_hex(data[2:3]))
        # # print('STX',STX,type(STX))
        # # print('data[2:3]报文开始02H:', data[2:3], str(binascii.b2a_hex(data[2:3])))
        #
        # BLOCK = int(data[3:8])
        # # print('BLOCK重量:',BLOCK)
        # # print('data[3:8]数据区:', int(data[3:8]), str(binascii.b2a_hex(data[3:8])))
        #
        # e = int(data[8:9])
        # # print('e:',e)
        # # print('data[8:9]重量值的阶码:', data[8:9], str(binascii.b2a_hex(data[8:9])))
        #
        # m = int(data[9:10])
        # # print('m:',m)
        # # print('data[9:10]动态检测位:', data[9:10], str(binascii.b2a_hex(data[9:10])))
        #
        # ETX = (data[10:11]).hex()
        # # print('ETX:',ETX)
        # # print('data[10:11]报文结束03H:', data[10:11], str(binascii.b2a_hex(data[10:11])))
        #
        # Bcc = str(binascii.b2a_hex(data[10:11]))
        # # print('data[11:12]信息块校验和:', data[11:12], str(binascii.b2a_hex(data[11:12])))
        #
        # LF = (data[12:13]).hex()
        # # print('LF:',LF)
        # # print('data[12:13]回车 0AH:', data[12:13], str(binascii.b2a_hex(data[12:13])))
        #
        # str_return_data = str(binascii.b2a_hex(data))
        #
        # # print('转换后str_return_data:', str_return_data, type(str_return_data))
        # strdw = str_return_data.find('014102')
        # # print('所在字符的位置', strdw)
        weightdict = {'42': weight_2liu}
        # elif SOH == '01' and ADDR == 42 and STX == 2 and m == 0 and ETX =='03' and LF == '0a':
        #     weightdict = {'42': BLOCK}
        # elif SOH == '01' and ADDR == 43 and STX == 2 and m == 0 and ETX =='03' and LF == '0a':
        #     weightdict = {'43': BLOCK}
        # elif SOH == '01' and ADDR == 44 and STX == 2 and m == 0 and ETX =='03' and LF == '0a':
        #     weightdict = {'44': BLOCK}
        time.sleep(60)
        return weightdict


if __name__ == "__main__":

    try:
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.bind(('', 20002))
        s1.listen(5)
        print("开始监听")
        while True:
            conn, addr = s1.accept()
            print(conn)
            print(addr)
            flag = True
            while flag:
                data = conn.recv(1024)
                if data:
                    # print(data)
                    # print('data:', data, type(data), len(data))
                    weightdict = {}
                    # print('原始数据', data)
                    # pro_data = binascii.b2a_hex(data)
                    # print('转换为十六进制', str(pro_data),type(pro_data),len(pro_data))
                    # print(data)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '二流重量', data)
                    with open('2233.txt', 'a+') as f:
                        f.writelines(
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '2传感器线程重量' + str(
                                binascii.b2a_hex(data)) + '\n')
                    print(data)
                    time.sleep(60)
                else:
                    flag =False

        s1.close()
    except Exception as e:
        print(e)


# str_data = str(data)
# print (str_data,type(str_data))
# str_ss = '\\x01\\x65\\x02'
# print (str_ss)
# print (str_data.find(str_ss))

# d = [chr(x) for x in bytes(data)]
# print (d)


# for x in bytes(data):
#     print(x,hex(x))


# b'\xf8\xfe\xf8\xf8\x00\x00'


# c = bytes(b'\x31\x32\x61\x62').decode('ascii')
# c = bytes(b'\xf8').decode('ascii')
# print (c)
# d = [hex(x) for x in bytes(b'\x01\x0212')]
# print (d)


# print("ASCII码", a, " 对应的字符为", chr(a))

'''
SOH 报文引导信息头 01H
ADDR 本显示器地址 41H
STX 报文开始 02H
5位重量数据
e 重量值的阶码。例重量值为500.0kg，以浮点数表示为0.05000×104，所以
e=4
m：动态检测位。称量处于动态m=1；称量处于稳定时m=0。
ETX 报文结束 03H
Bcc 信息块校验和 
LF 回车 0AH



字节串转字符串:
字节码解码为字符串: bytes(b'\x31\x32\x61\x62').decode('ascii')  ==>  12ab
字节串转16进制表示,夹带ascii: str(bytes(b'\x01\x0212'))[2:-1]  ==>  \x01\x0212
字节串转16进制表示,固定两个字符表示: str(binascii.b2a_hex(b'\x01\x0212'))[2:-1]  ==>  01023132
字节串转16进制数组: [hex(x) for x in bytes(b'\x01\x0212')]  ==>  ['0x1', '0x2', '0x31', '0x32']


'''
