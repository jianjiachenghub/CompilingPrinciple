#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>																/*添加头文件*/

int TESTmachine()
{
	int es = 0, i,codecount, stack[1000], stacktop = 0;
	char Codein[300], code[1000][20];
	int data[1000]; 															/*修改为int*/
	int label[100] = { 0 };
	char lno[4];
	FILE *fin;	//用于指向输入输出文件的指针
	if ((fin = fopen("D:\\middle.txt", "r")) == NULL)
	{
		printf("\n 打开D:middle.txt错误!\n", Codein);
		es = 10;
		return(es);
	}
	codecount = 0;
	fscanf(fin, "%s", &code[codecount]);										/*取消赋值给i*/
	while (!feof(fin))//程序文件读入
	{
//		printf("0000	%d	%s	\n", codecount, code[codecount]); 				/*无意义输出*/ 
		i = strlen(code[codecount]) - 1;  
		if (code[codecount][i] == ':')  //查找字符数组“label：”符号   存入是标签的位置 
		{
			i = i - 5;
			for (int j = 0; j < i; j++)
			{
				lno[j] = code[codecount][j+5];
			}
			lno[i] = '\0';
			label[atoi(lno)] = codecount;	
			printf("label[%d]= %d \n", atoi(lno), label[atoi(lno)]);
			code[codecount][i+5] = ':';
			code[codecount][i+6] = '\0';
			strcat(code[codecount], lno);
//			printf("test    %s\n", code[codecount]); 
//			k++;															/*k可能没有用*/
		}
		codecount++;
		fscanf(fin, "%s", &code[codecount]);   
	}
	fclose(fin);
	
//	for(i = 0; i < 10; i++)													/*无意义输出*/
//		printf("label%d %d \n", i, label[i]);
	
	for (i = 0; i < codecount; i++) { 
		int l;
		l = strlen(code[i]);
		if ((l > 1) && (code[i][1] == 'A')) {
			lno[0] = code[i][l - 1];
			lno[1] = '\0';
			itoa(label[atoi(lno)], code[i], 10);
		}
//		printf("%s\n", code[i]);                                         /********************/ 
	}
 	
// 	for(k = 0; i < 5; k++)													/*无意义输出*/
//	 	printf("label%d	%d	\n", k, label[k]); 
 	
	i = 0;
 
	while (i < codecount)	//执行每条指令
	{
//		printf("code % d %s \n", i,code[i]);
		if (strcmp(code[i], "LOAD") == 0)	  //LOAD D将D中的内容加载到操作数栈
		{
			i++;
			stack[stacktop] = data[atoi(code[i])];
			stacktop++;
		}
		else if (strcmp(code[i], "LOADI") == 0)	 //LOADI a将常量a压入操作数栈
		{
			i++;
			stack[stacktop] = atoi(code[i]);
			stacktop++;
		}
		//STO D将操作数栈栈顶单元内容存入D,且栈顶单元内容保持不变 
		else if (strcmp(code[i], "STO") == 0)
		{
			i++;
			data[atoi(code[i])] = stack[stacktop - 1];
//			printf("sto stack %d\n", stack[stacktop - 1]);
//			printf("sto data %d\n", data[atoi(code[i])]);
		}
		//POP桟顶单元内容出桟 
		else if (strcmp(code[i], "POP") == 0)
		{
			stacktop--;
		}
		//ADD将次桟顶单元与栈顶单元内容出栈并相加，和置于栈顶 
		else if (strcmp(code[i], "ADD") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] + stack[stacktop - 1];
//			printf("\t\tadd的结果 %d\n", stack[stacktop - 2]);  //输出和的值 					 
			stacktop--;
		}
		//SUB 将次栈顶单元减去栈顶单元内容并出栈，差置于栈顶 
		else if (strcmp(code[i], "SUB") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] - stack[stacktop - 1];
			stacktop--;
		}
		//MULT 将次栈顶单元与栈顶单元内容出栈并相乘，积置于栈顶 
		else if (strcmp(code[i], "MULT") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] * stack[stacktop - 1];
//			printf("\t\tmult结果 %d\n", stack[stacktop - 2]);  //输出乘的值 				
			stacktop--;
		}
		//DIV 将次栈顶单元与栈顶单元内容出栈并相除,商置于栈顶 
		else if (strcmp(code[i], "DIV") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] / stack[stacktop - 1];
			stacktop--;
		}
		//BR lab无条件转移到lab 
		else if (strcmp(code[i], "BR") == 0)
		{
			i++;
			i = atoi(code[i]);
		}
		//BRF lab检查栈顶单元逻辑值并出栈,若为假(0)则转移到lab 
		else if (strcmp(code[i], "BRF") == 0)
		{
			i++;
			if (stack[stacktop - 1] == 0) i = atoi(code[i]);
			stacktop--;
		}
		//EQ将栈顶两单元做等于比较并出栈,并将结果真或假(1或0)置于栈顶 
		else if (strcmp(code[i], "EQ") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] == stack[stacktop - 1];
			stacktop--;
		}
		//NOTEQ栈顶两单元做不等于比较并出栈，并将结果真或假(1或0)置于栈顶 
		else if (strcmp(code[i], "NOTEQ") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] != stack[stacktop - 1];
			stacktop--;
		}
		//GT 次栈顶大于栈顶操作数并出栈，则栈顶置1,否则置0 
		else if (strcmp(code[i], "GT") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] > stack[stacktop - 1];
			stacktop--;
		}
		//LES次桟顶小于栈顶操作数并出栈，则栈顶置1,否则置0 
		else if (strcmp(code[i], "LES") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] < stack[stacktop - 1];
			stacktop--;
		}
		//GE次栈顶大于等手栈顶操作数并出栈，则桟顶置1,否则置0 
		else if (strcmp(code[i], "GE") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] >= stack[stacktop - 1];
			stacktop--;
		}
		//LE次栈顶小于等于桟顶操作数并出栈，则栈顶置1,否则置0 
		else if (strcmp(code[i], "LE") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] <= stack[stacktop - 1];
			stacktop--;
		}
		//AND将栈顶两单元做逻辑与运算并出栈，并将结果真或假(1或0>置于栈顶 
		else if (strcmp(code[i], "AND") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] && stack[stacktop - 1];
			stacktop--;
		}
		//0R将栈顶两单元做逻辑或运算并出栈，并将结果真或假(1或0)置于栈顶 
		else if (strcmp(code[i], "OR") == 0)
		{
			stack[stacktop - 2] = stack[stacktop - 2] || stack[stacktop - 1];
			stacktop--;
		}
		//NOT将栈顶的逻辑值取反 
		else if (strcmp(code[i], "NOT") == 0)
		{
			stack[stacktop - 1] = !stack[stacktop - 1];
		}
		//IN从标准输入设备(键盘)读入一个整型数据,并入栈 
		else if (strcmp(code[i], "IN") == 0)
		{
			printf("请输入数据：");
			scanf("%d", &stack[stacktop]);
			stacktop++;
		}
		//OUT将栈顶单元内容出栈，并输出到标准输出设备上(显示器) 
		else if (strcmp(code[i], "OUT") == 0)
		{
		    i++;
			printf("程序输出结果： %d\n", stack[stacktop-1]);        
			stacktop--;
		}
		//STOP停止执行
		else if (strcmp(code[i], "STOP") == 0)
		{
		    printf("虚拟机运行成功\n");
			stack[stacktop] = '\n';
			return es=0;
		}
		i++;
	}
	return (es);
}
int main()
{
	int es = 0;
	es = TESTmachine();//调用抽象机代码运行模拟
}
