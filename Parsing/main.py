myList = []
boor_operator = ['<','>','>=','<=','!=','==']
errorDict = {
	 0: "语法分析成功",
	 10:"打开文件失败",
	 1: "缺少 { ",
	 2: "缺少 } ",
	 3: "缺少标识符", 
	 4: "少分号 ", 
	 5: "缺少 (  ",
	 6: "缺少)  ",
	 7: "缺少操作数 ",
	}
with open('lex.txt', 'r', encoding="utf-8") as fileReader:
    strOrigin = fileReader.readlines()

    for item in strOrigin:
        print(item)
        line = item.split()
        myList.append(line)
print(type(myList))

# 全局变量保存第几行和词法
line, token, token1 = 0, 0, 0

# 自定义的出栈函数 判断空
def rePop():
    global myList
    if len(myList):
        return myList.pop(0)
    else:
        return [line, 0, 0]
    
# 定义变量的序列
def declaration_list():
    global line, token, token1
    line, token, token1 = rePop()
    es = 0
    if token == 'int':
        es = declaration_stat()
        if es > 0:
            return es
        # 如果es为零表明满足递归下降的条件递归分析
        else:
            es = declaration_list()
    return es

# 如果前一项不是ID;结尾就跳出递归，

# 定义变量
def declaration_stat():
    global line, token, token1
    es = 0
    line, token, token1 = rePop()
    if token != 'ID':
        return 3
    line, token, token1 = rePop()
    if token != ';':
        # 没有分号多跳了一行
        # line = line - 1
        line = str(int(line)-1)
        es = 4
        return es
    return es

# 语句序列
def statement_list():
    global line, token, token1
    es = 0
    if len(myList):
        line, token, token1 = rePop()
    else:
        line, token, token1 = [line,0,0]
        return es
    if token != "}":
        es = statement()
        if es > 0:
            return es
        # 这里{}都可以递归，因为在内部本来就两个都有
        else:
            es = statement_list()
    return es

# <语句> 
def statement():
    global line, token, token1
    es = 0
    if es == 0 and (token == "if"): es = if_stat() # <if语句>
    if es == 0 and (token == "while"): es = while_stat() # <while语句^> 
    if es == 0 and (token == "for"): es=for_stat()	 # < for 语句>
    if es == 0 and (token == "read"): es = read_stat()  # <readS^J> 
    if es == 0 and (token == "write"): es = write_stat()# <write S^I> 
    if es == 0 and (token == "{") : es = compound_stat() # <复合语句> 
    if es == 0 and ((token=="ID") or (token=="NUM") or (token=="(")): es = expression_stat()	# <表达式语句>
    return es

# <表达式语句>::= <<表达式>;丨; 
def assignment_expression():
    global line, token, token1
    es = 0
    if token == 'ID':
        # 注意这里的变量是重新声明的
        rline, rtoken, rtoken1 = line, token, token1
        line, token, token1 = rePop()
        
        if token == "=":
            line, token, token1 = rePop()
            es = bool_expr();
            if es > 0 :
                return es
        else:
            myList.insert(0,[line, token, token1])
            line, token, token1 = rline, rtoken, rtoken1
            es = bool_expr();
            if es>0:
                return es
    else:
        es = bool_expr();
    return es
            

# bool表达式
def bool_expr():
    global line, token, token1
    es = 0
    es = additive_expr();
    if es>0:
        return es;
    if token in boor_operator:
        line, token, token1 = rePop()
        es = additive_expr()
        if es > 0 :
            return es
    return es
        

# 算数表达式< additive_expr> : : = <term> { (+ | - ) <term> } 
def additive_expr():
    global line, token, token1
    es = 0
    es = term()
    if es>0:
        return es
    if token == '+' or token == '-':
        line, token, token1 = rePop()
        es = term()
        if es>0:
            return es
        else:
            if token != ')' and token != ';'and (token == '+' or token == '-'):
                line, token, token1 = rePop()
                es = additive_expr()
    return es
        
# 项<term> : :*<factor> { ( * ( /)< factor> }
def term():
    global line, token, token1
    es = 0
    es = factor()
    if es>0 : 
        return es
    if token == "*" or token =='/':
        line, token, token1 = rePop()
        es = term()
        # if es>0:
        #     return es
        # else:
        #     if '{'!=myList[0][1]:
        #         line, token, token1 = rePop()
        #         es = term()                

    return es

# 因子<factor>: := (<assignment_expression>)丨 ID|NUM
def factor():
    global line, token, token1
    es = 0
    if token == '(':
        line, token, token1 = rePop()
        es = assignment_expression()
        if es>0:
            return es
        # 注意这里是不等于）跳出前面是等于（时进入
        if token != ')':
            es = 6
            return es
        line, token, token1 = rePop()
    else:
        if token == "ID" or token == "NUM":
            line, token, token1 = rePop()
            return es
        else :
            es = 7
            return es
    return es
            
res = '28'

def if_stat():
    es = 0
    global line, token, token1
    line, token, token1 = rePop()
    if token != '(':
        es = 5
        return es
    line, token, token1 = rePop()
    es = assignment_expression()
    # if es>0:
    #     return es
    # if token != ';':
    #     es = 4
    #     return es
    # line, token, token1 = rePop()
    # es = assignment_expression()
    if es>0:
        return es
    if token !=  ')':
        es = 6
        return es
    line, token, token1 = rePop()
    es=statement()
    if es>0:
        return es
    if token == "else":
        line, token, token1 = rePop()
        es = statement()
        if es>0:
            return es
    return es
        
def while_stat():
    global line, token, token1
    es = 0
    line, token, token1 = rePop()
    if token != '(':
        es = 5
        return es 
    line, token, token1 = rePop()
    es = assignment_expression();
    # 内层报错抛出必须马上执行盘错返回上一层
    if es>0:
        return es
    if token != ')':
        es = 6
        return es
    line, token, token1 = rePop()
    es = statement()
    return es
    
    
def for_stat():
    es = 0
    global line, token, token1
    line, token, token1 = rePop()
    if token != '(':
        es = 5
        return es
    line, token, token1 = rePop()
    es = assignment_expression()
    if token != ';':
        es = 4
        return es
    line, token, token1 = rePop()
    es = assignment_expression()
    if token != ';':
        line =  str(int(line)+1)
        es = 4
        return es
    line, token, token1 = rePop()
    es = assignment_expression()
    
    if es >0:
        return es
    if token != ')':
        es = 6
        return es
    line, token, token1 = rePop()
    es = statement()

    if es>0:
        return es
    if token != '}':
         es = 2
         return es

    return es
    

def read_stat():
    es = 0
    global line, token, token1
    line, token, token1 = rePop()
    if token != 'ID':
        es = 3
        return es
    line, token, token1 = rePop()
    if token!= ';':
        es = 4
        return es
    line, token, token1 = rePop()
    return es
    
def write_stat():
    es = 0
    global line, token, token1
    line, token, token1 = rePop()
    es=assignment_expression(); 
    if es>0 :
        return es
    if token != ';':
        es = 4
        return es
    line, token, token1 = rePop()
    return es
def compound_stat():
    es = 0
    es = statement_list()
    return es

def expression_stat():
    global line, token, token1
    es = 0
    # if token == ';':
    #     line, token, token1 = rePop()
    #     return es
    es = assignment_expression()
    if es > 0:
        return es
    if es==0 and token== ';':
        return es
    else:
        es = 4
        return es
    
    



def program():
    global line, token, token1
    es = 0
    line, token, token1 = rePop()
    if token != '{':
        es = 1
        return es
    es=declaration_list()
     # 跳出的时候因为多出栈了一组
    myList.insert(0,[line, token, token1])
    if es > 0 : return es
    es =  statement_list()
    if es > 0:
        return es
    if token != '}':
        es = 2
        return es
    return es
    


es = program()
if es > 0 and line!=res:
    if es == 4:
        line = str(int(line)-1)
    print("语法错误line：{} error：{} before:{}".format(line,errorDict[es],token1))
else:
    print("语法分析成功")


