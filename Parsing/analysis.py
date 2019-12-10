import re

# 保留字
reserveWord = ["if", "else", "for", "int", "while", "int","write", "read"];

# 先区分单双分解符来确定是否需要多取一个字符
delimiter = ['=','+','-','*','/','(',')',';','{','}',':',',',';',';','<','>','!']

singleDelimiter = ['(',')',';','{','}']

doubleDelimiter = ['>=','<=','!=','==']

# 然后在和运算符对比，区分运算符和分解符
operator = ['+','-','*','/','=','<','>','>=','<=','!=','==']



# 过滤掉单行注释和换行符
def filterOrigin(str):
    filterstr = re.sub(r'\/\*[\s\S]*\*\/|\/\/.*','',str)
    filterstr = filterstr.replace('\n','')
    filterstr = filterstr.replace('\t','')
    return filterstr

# 保存总错误


# 处理多行注释和不合法的注释    
def cleanComment(strLines):
    global errorSum
    errorSum = 0
    for str in strLines:
        # 记录第一个/*出现在第几行的第几列
        startIndexCol  = str.find('/*')
        if startIndexCol>=0:
           startIndexRow =  strLines.index(str)
           strLines[startIndexRow] = strLines[startIndexRow][0:startIndexCol]
           print(strLines[startIndexRow])
           
           # '/*' 记录成功后往后匹配 '*/',然后记录出现行列
           for index in range(startIndexRow,len(strLines)):
                endIndexCol = strLines[index].find('*/')
                if endIndexCol>=0:
                    # */是往后取值，拿到的是*的位置，所以需要+2
                    endIndexCol+=2
                    endIndexRow =  index
                    endRowLen = len(strLines[endIndexRow])
                    strLines[endIndexRow] = strLines[endIndexRow][endIndexCol:endRowLen+1]
                    print(strLines[endIndexRow])
                    # 跨越行的/* */之间的内容置空，不能删除，控制总行数不变，不然影响遍历序列
                    for i in range(startIndexRow+1,endIndexRow):
                        strLines[i] = ''
                    # 寻找到'*/'执行相关操作后需要打断循环，从下一行字符开始遍历
                    break
                # 当最后一行还未找到'*/'则为不合法的注释
                elif index==len(strLines)-1:
                    endIndexRow = len(strLines)
                    # 置空未闭合的'/*'后面的一切行，包括最后一行 
                    # startIndexRow+1是因为，本行要被截取有效的部分
                    for i in range(startIndexRow+1,endIndexRow):
                        strLines[i] = ''
                    errorSum+=1
                    print("在第{}行发生词法错误,错误信息：注释不合法".format(startIndexRow+1))
                    
           
           
        
    
# 全局变量，保存token
tokenList = []



# 读取文件为一个字符串
with open('origin.txt', 'r') as fileReader:
    strOrigin = fileReader.readlines()
    print(type(strOrigin))
    strLines = list(map(filterOrigin,strOrigin))
    print(strLines)

cleanComment(strLines)

index = 0

# 按行读取
for str in strLines:
    index = index + 1
    # 字符串转为列表
    strList = list(str)
    while len(strList):
        char = strList.pop(0)
        
        # 分析保留字与标识符
        if char.isalpha():
            token = {
                "type":"标识符", 
                "name":""
            }
            token['name'] += char
            
            # 这里没有判断一行只有一个字母或者数字的情况，如果有则可以直接跳过该行，提示语法错误 
            # 循环读取下一个字符，当下一个字符非字母数字终止或者，栈空终止读入
            if len(strList):
                char = strList.pop(0)
      
                while char.isalnum():
                    token['name'] += char
                    if len(strList):
                        char = strList.pop(0)
                    else:
                        break
                    
                # while 循环被不是字母数字的打断，就会多出栈一个非数字和字母的，这里需要重新入栈
                if not char.isalnum():
                    strList = [char]+strList

                # 判断字符类型      
                if token['name'] in reserveWord:
                    token['type'] = '保留字'
                else:
                    token['type'] = '标识符'
            # 保存到全局变量里
            token['line'] = index
            tokenList.append(token)
            
        # 分析无符号整数 算法与上一步类似   
        elif char.isdigit():
            token = {
                "type":"",
                "name":""
            }
            token['name'] += char
            char = strList.pop(0)
            while char.isdigit():
                token['name'] += char
                if len(strList):
                    char = strList.pop(0)
                else:
                    break
                
            if not char.isdigit():
                strList = [char]+strList
            
            token['type'] = '无符号整数'
            token['line'] = index
            tokenList.append(token)
            

                
        elif char in singleDelimiter:
            token = {
                "type":'分界符',
                "name":char
            }
            token['line'] = index
            tokenList.append(token)
        # 判断单分解符和多分界符
        elif (char in operator) or char == '!':
            token = {
                "type":'',
                "name":''
            }
            if len(strList):
                # 暂时取值，并未出栈
                char2 = strList[0]
                doubleChar = char+char2
                if doubleChar in operator:
                    # 双分界符多出栈一个
                    char = strList.pop(0)
                    # 进一步分类，判断运算符
                    isOperator = doubleChar in operator
                    # python三目运算 有点不一样
                    token['type'] = '运算符'
                    token['name'] = doubleChar
                elif char in operator:
                    token['type'] = '运算符'
                    token['name'] = char

                else:
                    errorSum+=1
                    print("在第{}行发生词法错误,错误信息：{}不合法".format(index,char))
                    continue
            elif char in operator:
                token['type'] = '运算符'
                token['name'] = char
            else:
                errorSum+=1
                print("在第{}行发生词法错误,错误信息：{}不合法".format(index,char))
                continue
            token['line'] = index           
            tokenList.append(token)
            
        # 判断错误代码
        elif char!=' ':
            errorSum+=1
            print("在第{}行发生词法错误,错误信息：{}未知符号".format(index,char))

with open('lex.txt', 'w',encoding='utf-8') as writer:
    for token in tokenList:
        if token['type'] == '标识符':
            writer.writelines('{} {} {}\n'.format(token['line'],'ID',token['name']))
        elif token['type'] == '保留字' or token['type'] == '运算符':
            writer.writelines('{} {} {}\n'.format(token['line'],token['name'],token['name']))
        elif token['type'] == '无符号整数':
            writer.writelines('{} {} {}\n'.format(token['line'],'NUM',token['name']))
        elif token['type'] == '分界符':
            writer.writelines('{} {} {}\n'.format(token['line'],token['name'],token['name']))
        
print("总共发生了{}次词法错误".format(errorSum))       
print(tokenList)
              
