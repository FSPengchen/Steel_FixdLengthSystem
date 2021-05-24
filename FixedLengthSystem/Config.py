import os
import configparser

class Config():
    def __init__(self):
        self.path = r"E:\PycharmProjects\FixedLengthSystem"
        self.pathconfig =r'E:\PycharmProjects\FixedLengthSystem\config.ini'
        print('初始化')

    def readTest(self):
        os.chdir(r"E:\PycharmProjects\FixedLengthSystem")
        cf = configparser.ConfigParser()
        # read(filename) 读文件内容
        filename = cf.read("config.ini", encoding="utf-8")
        print(filename)

        # sections() 得到所有的section，以列表形式返回
        sec = cf.sections()
        print(sec)

        # options(section) 得到section下的所有option
        opt = cf.options("init")
        print(opt)

        # items 得到section的所有键值对
        value = cf.items("init")
        print(value)

        # get(section,option) 得到section中的option值，返回string/int类型的结果
        mysql_host = cf.get("init", "Btn_Class")
        mysql_password = cf.getint("init", "Lab_talRoot")
        print(mysql_host, mysql_password)

    '''
    cf.read(filename)：读取文件内容

    cf.sections()：得到所有的section，并且以列表形式返回
    
    cf.options(section)：得到section下所有的option
    
    cf.items(option)：得到该section所有的键值对
    
    cf.get(section,option)：得到section中option的值，返回string类型的结果
    
    cf.getint(section,option)：得到section中option的值，返回int类型的结果
    '''

    def readAllSection(self):
        os.chdir(r"E:\PycharmProjects\FixedLengthSystem")
        cf = configparser.ConfigParser()
        cf.read("config.ini", encoding="utf-8")
        reslut = cf.sections()
        return reslut


    def readvalue(self,section,option, encoding = "utf-8"):
        # 创建管理对象
        cf = configparser.ConfigParser()
        # 读ini文件
        cf.read(self.pathconfig, encoding) # python3
        reslut = cf.get(section,option)
        return reslut



    def writeTest(self):   #新建配置文件，写入文件

        os.chdir(r"E:\PycharmProjects\FixedLengthSystem")
        cf = configparser.ConfigParser()

        # 往配置文件写入内容

        # add section 添加section项
        # set(section,option,value) 给section项中写入键值对
        cf.add_section("mq")
        cf.set("mq", "user", "laozhang")
        cf.set("mq", "user", "aaa")
        cf.add_section("kafka")
        cf.set("kafka", "user", "xiaozhang")
        cf.add_section("kka")
        # write to file
        with open("config1.ini", "w+") as f:
            cf.write(f)

    def writeValue(self,section,option,value,encoding = "utf-8"):

        os.chdir(self.path)
        cf = configparser.ConfigParser()
        cf.read(self.pathconfig,encoding)
        cf.set(section,option,value)

        with open("config.ini","r+",encoding= "utf-8") as f:
            cf.write(f)




    def add_section(self,section):  # add section 添加section项
        os.chdir(r"E:\PycharmProjects\FixedLengthSystem")
        cf = configparser.ConfigParser()
        cf.add_section(section)
        with open("config1.ini", "w+") as f:
            cf.write(f)

    '''
    cf.write(filename)：将configparser对象写入.ini类型的文件

    add_section()：添加一个新的section
    
    add_set(section,option,value)：对section中的option信息进行写入
    '''

    def writeChangeTest(self):
        try:
            os.chdir(r"E:\PycharmProjects\FixedLengthSystem")
        except FileNotFoundError:
            print("未找到该文件")
        else:
            cf = configparser.ConfigParser()
            # 修改配置文件的内容
            # remove_section(section)  删除某个section的数值
            # remove_option(section,option) 删除某个section下的option的数值
            cf.read("config1.ini")
            cf.remove_option("kafka", "user")
            cf.remove_section("mq")
            # write to file
        try:
            with open("config1.ini", "w+") as f:
                cf.write(f)
        except FileNotFoundError:
            print("未找到该文件")

    '''
    cf.read(filename)：读取文件（这里需要注意的是：一定要先读取文件，再进行修改）

    cf.remove_section(section)：删除文件中的某个section的数值
    
    cf.remove_option(section,option)：删除文件中某个section下的option的数值
    '''

    def print1(self):
        print("有反应")

if __name__ == "__main__":
    config = Config()
    #config.writeValue('init', 'smtp_vserver','啊 啊')
    #print(config.readvalue('init', 'smtp_vserver'))





'''
Python-with open() as f的用法

with open(r'filename.txt') as f:
   data_user=pd.read_csv(f)  #文件的读操作

with open('data.txt', 'w') as f:
   f.write('hello world')  #文件的写操作
   
   
r:	以只读方式打开文件。文件的指针将会放在文件的开头。这是**默认模式**。
rb: 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
r+: 打开一个文件用于读写。文件指针将会放在文件的开头。
rb+:以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
w:	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb:	以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
w+:	打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb+:以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
a:	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab:	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+:	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+:以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。

————————————————

file.read([size])   将文件数据作为字符串返回，可选参数size控制读取的字节数
file.readlines([size])   返回文件中行内容的列表，size参数可选
file.write(str)   将字符串写入文件
file.writelines(strings)   将字符串序列写入文件
file.close()   关闭文件
file.closed	表示文件已经被关闭，否则为False

file.mode	Access文件打开时使用的访问模式
file.encoding	文件所使用的编码
file.name	文件名
file.newlines	未读取到行分隔符时为None，只有一种行分隔符时为一个字符串，当文件有多种类型的行结束符时，则为一个包含所有当前所遇到的行结束的列表
file.softspace	为0表示在输出一数据后，要加上一个空格符，1表示不加。这个属性一般程序员用不着，由程序内部使用
————————————————


'''