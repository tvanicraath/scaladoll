import os


class To_real_ir:
	def __init__(self):
		print "initiated ir code generation"
		self.memory_dict={}
		self.temp_var_dict={}
		self.temp_var_dict_reverse={}
		self.temp_label_dict={}
		self.temp_label_dict_reverse={}
		self.iflist=[]
#		self.var_dict2={}
		self.temp_varnum=1
		self.temp_label=1
		self.processing_line=0
		os.remove("IR.ll")
		self.ll_file = open("IR.ll", "w")
		self.ll_file.write("; ModuleID = 'test.c'\ntarget datalayout = \"e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128\"\ntarget triple = \"x86_64-pc-linux-gnu\"\n")
		self.ll_file.write("define i32 @main() nounwind uwtable {\n")
		self.start()
		self.ll_file.write("ret i32 0\n}\n")
		self.ll_file.close()

	def start(self):
		print "Started"
		#line0=[("int","Int_RET_TYPE"),("main","FUNC_NAME")]
#		linex=[("{","OPEN_CURLY_BRACE")]
		#line2=[("y@@","VAR"),(":=","ASSIGN"),("@z6","VAR"),("+","ADD"),("6","Int")]
#		line1=[("@z6","VAR"),(":=","COPY"),("3","Int")]
#		line2=[("y@@","VAR"),(":=","COPY"),("3","Int")]
#		line3=[("m","VAR"),(":=","ASSIGN"),("@z6","VAR"),(">","ADD"),("y@@","VAR")]
#		line4=[('m', 'VAR'), ('?', 'IF'), ('->', 'GOTO'), ('LABEL', 'L128')]
		lines=[((('t@@119', 'VAR'), (':=', 'COPY'), ('a@102', 'VAR')), 'COPY'),
((('t@@120', 'VAR'), (':=', 'COPY'), ('t@@119', 'VAR')), 'COPY'),
((('t@@121', 'VAR'), (':=', 'COPY'), (u'0', 'VAR')), 'COPY'),
((('t@@122', 'VAR'), (':=', 'COPY'), ('t@@121', 'VAR')), 'COPY'),
((('t@@123', 'VAR'), (':=', 'ASSIGNMENT'), ('t@@120', u'VAR'), (u'!=', 'OPR'), ('t@@122', 'VAR')), 'ASSIGNMENT'),
((('t@@123', 'VAR'), ('?', 'IF'), ('->', 'GOTO'), ('LABEL', 'L126')), 'IF'),
((('->', 'GOTO'), ('LABEL', 'L125')), 'GOTO'),
((('L', 'LABEL'), ('LABEL', 'L126')), 'LABEL'),
((('L', 'LABEL'), ('LABEL', 'L125')), 'LABEL')]
#		liney=[("}","CLOSE_CURLY_BRACE")]
		#lines=[(line0,"FUNC_DECL"),(linex,"START"),(line1,"COPY"),(line2,"ASSIGNMENT"),(line3,"ASSIGNMENT"),(liney,"FINISH")]
#		lines=[(line1,"COPY"),(line2,"COPY"),(line3,"ASSIGNMENT"),(line4,"IF")]
		temp=1;

		for i in range(0,len(lines)):
			self.processing_line=i
			self.processline(lines[i])
			

# processing each line in the three address code
	def processline(self,line_full):
		
		(statement,attribute1)=line_full
		start=0
		line=statement
		line_type=attribute1
		if(line_type=="ASSIGNMENT"):
			line_vars=[]
			print line
			print line[start]
			ops=[">","==","<",">=","<=","!="]
                        s=set(ops)
                        type_flag=0
			(oper,op)=line[start+3]
                        if oper in s:
                                type_flag=1
			

## term 1
			(x1,y1)=line[start]
			if(type_flag==0):
				self.allot_memory(x1)
			else:
				self.allot_memory(x1,"Bool")
			#line_vars.insert(0, x1)
## term 2
			(x2,y2)=line[start+2]
			if(y2=="Int"):
				temp2=x2
			else:
				temp2=self.load(x2)
			line_vars.append(temp2)
## term 3
			(x3,y3)=line[start+4]
			if(y3=="Int"):
                                temp3=x3
                        else:
                                temp3=self.load(x3)
			line_vars.append(temp3)

			operator="BINARY"
	

#new temp variable for operation
			temp1=self.temp_varnum
			self.temp_varnum+=1
			line_vars.insert(0, temp1)
				
			dict_temp = {temp1: 0}
			self.temp_var_dict_reverse.update(dict_temp)

			if(oper=="+"):
				op="ADD"
			if(oper=="-"):
				op="SUB"
			if(oper==">"):	
				op="GT"
			if(oper=="<"):
				op="LT"
			if(oper==">="):
				op="GTE"
			if(oper=="<="):	
				op="LTE"
			if(oper=="=="):
				op="EQ"
			if(oper=="!="):
				op="NE"

			if(operator=="BINARY"):
				printop="undefined"
				flag=0
				if(op=="ADD"):
					printop="add"
					#self.ll_file.write("%"+line_vars[0]+" = "+printop+" i32 "+self.print_by_type(line_vars[1])+" "+print_by_type(line_var[2])+"\n")
					flag=1
				if(op=="SUB"):
					printop="sub"
					flag=1
				if(flag==1):
					print line_vars
					self.ll_file.write("%"+str(line_vars[0])+" = "+printop+" nsw i32 "+self.print_by_type(line_vars[1],y2)+","+self.print_by_type(line_vars[2],y3)+"\n")
					self.ll_file.write("store i32 "+self.print_by_type(line_vars[1],y2)+", i32* "+self.print_by_type(line_vars[2],y3)+"\n")
				if(op=="GT"):
					llvm_oper="sgt"
					flag=2
				if(op=="LT"):
					llvm_oper="slt"
					flag=2
				if(op=="EQ"):
					llvm_oper="eq"
					flag=2
				if(op=="GTE"):
					llvm_oper="sge"
					flag=2
				if(op=="LTE"):
					llvm_oper="sle"
					flag=2
				if(op=="NE"):
					llvm_oper="ne"
					flag=2
				if(flag==2):
					self.iflist.append(line_vars)	
					self.ll_file.write("%"+str(line_vars[0])+" = icmp "+llvm_oper+" i32 "+self.print_by_type(line_vars[1],y2)+", "+self.print_by_type(line_vars[2],y3)+"\n")
					self.ll_file.write("store i32 %"+str(line_vars[0])+", i1* %\""+x1+"\"\n")
		#l1=self.generate_label()

					#self.ll_file.write("br i1 %"+self.print_by_type(line_vars[0],y1)+", label %"+l1+", label %"+l2+"\n")
					#self.ll_file(l1+)
					
	
		if(line_type=="COPY"):
			(x1,y1)=line[start]
			(x2,y2)=line[start+2]

#allot memory to x1			
			self.allot_memory(x1)

			if(y2=="Int"):
                                temp2=x2
                        else:
                                temp2=self.load(x2)

			self.ll_file.write("store i32 "+self.print_by_type(temp2,y2)+", i32* "+self.print_by_type(x1,y1)+"\n") 
			
		if(line_type=="LABEL"):
			(y1,label_name)=line[start+1]
			#(x2,y2)=line[start+1]
			if(y1=="LABEL"):
				self.ll_file.write(label_name+":\n")
			else:
	#			print "error in label"
				raise AssertionError("Error in LABEL")
			

		if(line_type=="IF"):	
			#self.ll_file.write("IN If\n")	
			(x1,y1)=line[start]
			line_vars=[]
			if(y1=="Int"):
                                temp1=x1
                        else:
                                temp1=self.load(x1,"Bool")
			line_vars.append(temp1)
			print "yeah"+str(line_vars)
			(y2,label_name)=line[start+3]
			l1=self.generate_label()
			l2=self.generate_temp_label(label_name)
                        self.ll_file.write("br i1 "+self.print_by_type(line_vars[0],y1)+", label %"+l1+", label %"+l2+"\n")
			self.print_label(l1)

                        #self.ll_file(l1+)

		if(line_type=="FUNC_DECL"):
			(x1,y1)=line[start]
			handle_return_type(y1)
			(x2,y2)=line[start+1]	
			if(y2=="FUNC_NAME"):
				self.ll_file.write("@"+x2+"() nounwind uwtable")
			
		
	def load(self,var_name,var_type="Int"):
		dict2={var_name: self.temp_varnum}
		#print dict2
		self.temp_var_dict.update(dict2)
		dict2={self.temp_varnum: var_name}
		self.temp_var_dict_reverse.update(dict2)
		if(var_type=="Int"):
			real_type="i32"
		elif(var_type=="Bool"):
			real_type="i1"
			
	 	self.ll_file.write("%"+str(self.temp_varnum)+" = load "+real_type+"* %\""+var_name+"\"\n")	
		self.temp_varnum+=1
		return self.temp_varnum-1
	

	def print_by_type(self,var_name,isvar):
		if(isvar=="Int"):
                        return str(var_name)
                elif(isvar=="VAR"):
			print var_name
			correct_name=self.check_var_if_tempvar_or_not(var_name)
			print correct_name
			return "%"+correct_name


	def check_var_ex(self,variable_name):
		if(not(self.memory_dict.has_key(variable_name))):
			return variable_name
		else:
			return self.temp_var_dict.get(variable_name)


	def add_temp_var(self,variable_name):
                if(not(self.temp_var_dict.has_key(variable_name))):
                        dict_temp = {variable_name: self.temp_varnum}
#                       dict_temp2 = {self.temp_varnum}
                        temp_varnum=self.temp_varnum
                        self.temp_varnum+=1
                        self.temp_var_dict.update(dict_temp)
			self.allot_memory(str(temp_varnum))
                        self.allot_memory(variable_name)
			self.assign_temp(variable_name,str(temp_varnum))

                        return str(temp_varnum)
                else:
                        return self.var_dict.get(variable_name)

	def generate_temp_label(self, label_name):
                if(not(self.temp_label_dict.has_key(label_name))):
                        dict_temp = {label_name: self.temp_label}
                        temp_label=self.temp_label
                        self.temp_label+=1
                        self.temp_label_dict.update(dict_temp)
                        return str(temp_label)
                else:
                        return self.label_dict.get(label_name)

	def generate_label(self):
		label=self.temp_label
		self.temp_label+=1
		return str(label)

	def handle_return_type(self,returntype):
		if(returntype=="Int_RET_TYPE"):
			self.ll_file.write("define i32 ");

# allot memory to variables			
	def allot_memory(self,variable_name,var_type="Int"):

		#check if memory already given
		if(not(self.memory_dict.has_key(variable_name))):
			#assuming that the variable is an integer i32
			if(var_type=="Int"):
                                real_type="i32"
                        elif(var_type=="Bool"):
                                real_type="i1"

			self.ll_file.write("%\""+variable_name+"\" = alloca "+real_type+"\n")
			dict2={variable_name:1}
			self.memory_dict.update(dict2)

# assign variables to temporary variables
	def assign_temp(self, variable_name,temp_var_name):
		correct_name=self.check_var_if_tempvar_or_not(temp_var_name)
		self.ll_file.write("store i32 %"+correct_name+", i32* %"+var_name+"\n")
	
	def check_var_if_tempvar_or_not(self, var_name):
		 
		 if(self.temp_var_dict_reverse.has_key(var_name)):
			print "if"
                 	return str(var_name)
                 else:
			print "else"
                 	return "\""+str(var_name)+"\""

	def print_label(self,label_var):
		self.ll_file.write("; <label>:"+label_var+"\n");

		
def main():
	print "in Main"
	iR=To_real_ir()
	print "finished"

if __name__ == "__main__":
	main()
