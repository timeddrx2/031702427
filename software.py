import jieba
import re
import json


outcome = []  #最后的结果

def slip():
    txt = open('software.txt',encoding = 'utf-8')
    while 1:
        s = txt.readline()
        if not s:
            break
        s = s.strip() #读取文件后面会自动加空格 此为去掉空格
        #s = "张三,福建福州闽13599622362侯县上街镇福州大学10#111"
        #print(add_imfo)    
        name = ''
        mydict = {"姓名":"","手机":"","地址":""}
        for i in s:
            if i != ',':
                name += i
                s = s[1:]
            else:
                s.strip(',')
                s = s[1:]
                break
        #print(s)
        mydict['姓名'] = name
        word = ''  #连接字符串
        add_imfo = jieba.lcut(s)  #切成一个列表
        #print(add_imfo)
        for item in add_imfo:  #遍历这个列表
            ret = re.match(r"1[35678]\d{9}", item)
            if ret:
                mydict['手机'] = item
                #print(item)
                #add_imfo.remove(item)#移除手机号
                continue
            word = word + item #地址合成
        #print(word)
        add_imfo = jieba.lcut(word)  #再切
        #print(add_imfo)
        #mydict['地址']  = add_imfo
        address = []
        #分省，直辖市；市
        if add_imfo[0] == '北京' or add_imfo[0] == '上海' or add_imfo[0] == '天津' or add_imfo[0] == '重庆':   #省市
            address.append(add_imfo[0])
            address.append(add_imfo[0] + '市')
            #print(add_imfo[0])
            add_imfo.remove(add_imfo[0])
        elif add_imfo[0] == '北京市' or add_imfo[0] == '上海市' or add_imfo[0] == '天津市' or add_imfo[0] == '重庆市':
            address.append(add_imfo[0][0:2])
            address.append(add_imfo[0])
            add_imfo.remove(add_imfo[0])
        else:
            address.append(add_imfo[0][0:2] + '省')
            add_imfo.remove(add_imfo[0])
            address.append(add_imfo[0][0:2] + '市')
            add_imfo.remove(add_imfo[0])
        #分区，自治州，县，自治县
        l = len(add_imfo[0])
        if add_imfo[0][l-1:l] == '县' or add_imfo[0][l-1:l] == '区' or add_imfo[0][l-1:l] == '州':
            address.append(add_imfo[0])
            add_imfo.remove(add_imfo[0])
        else:
            address.append('')
    
        #分镇，街，道，乡///////错误
        l = len (add_imfo[0])
        l1 = len(add_imfo[1])
        if add_imfo[1][l1-1:l1] == '镇' or add_imfo[1][l1-1:l1] == '道' or add_imfo[1][l1-1:l1] == '乡':
            address.append(add_imfo[0] + add_imfo[1])
            add_imfo.remove(add_imfo[0])
            add_imfo.remove(add_imfo[0])
        elif add_imfo[0][l-1:l] == '镇' or add_imfo[0][l-1:l] == '道' or add_imfo[0][l-1:l] == '乡':
            address.append(add_imfo[0])
            add_imfo.remove(add_imfo[0])
        else:
            address.append('')
    
        #增加最后地址
        Address = ''
        for item in add_imfo:
            Address += item
        address.append(Address)
        mydict["地址"] = address
        outcome.append(mydict)
        #已经得出一个完整的列表
    
#s = f.readline()
#s = ''
#s += line
slip()

json = json.dumps(outcome, ensure_ascii=False,indent=2)
print(json)