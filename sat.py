import re
import copy

def parse(filename):
    f = open(filename)
    line = f.readline().strip()
    inputs = re.split(r"[,]",line)
    list_clause = []
    print("input = " + str(inputs))

    line = f.readline().strip()
    while line != "":
        x= re.split(r"[+]",line)
        list_clause.append(x)
        line = f.readline().strip()
    f.close()
    return inputs,list_clause

sat = True
inputs,list_clause = parse('input.txt')
assgn_done = []
assgn = [False]*len(inputs)
done = False

def unit_clause(u_clauses,u_assigned,u_assign):
    u_done = False
    u_sat = False
    dummy_clause = copy.deepcopy(u_clauses) # Copy the list   
    for clause in dummy_clause:
        if len(clause) == 1:
            if clause[0] in inputs:
                index = inputs.index(clause[0])
                if index in u_assigned and u_assign[index] == False:
                    u_done = True
                    u_sat = False    
                elif not(index in u_assigned):
                    u_assign[index] = True
                    u_assigned.append(index)        
            else :
                index = inputs.index(clause[0][:-1])
                if index in u_assigned and u_assign[index] == True:
                    u_done = True
                    u_sat = False    
                elif not(index in u_assigned):     
                    u_assign[index] = False
                    u_assigned.append(index) 

            index_clause = u_clauses.index(clause)
            del u_clauses[index_clause]
    
    return u_sat,u_clauses,u_assigned,u_assign,u_done
                   
def pure_literal(list_clause,assgn_done,assgn):
    for literal in inputs :
        index = inputs.index(literal)
        if not(index in assgn_done):
            literal_val = False
            flag = 0 
            literal_bar = literal + "'"
            pure = []
            dummy_clause = list(list_clause) # Copy the list
            for clause in dummy_clause:
                if flag == 0 :
                    if literal in clause :
                        literal_val = True
                        flag = 1
                        pure.append(clause)
                    elif literal_bar in clause:
                        literal_val = False
                        flag = 1
                        pure.append(clause)
                elif flag == 1:
                    if literal in clause and literal_val == True:
                        pure.append(clause)
                    elif literal_bar in clause and literal_val == False :
                        pure.append(clause)
                    elif not(literal in clause) and not(literal_bar in clause) :
                        abcd = True
                    else :
                        pure = []
                        break
            
            if len(pure) != 0:
                assgn[index] = literal_val
                assgn_done.append(index)
                for y in pure :
                    index_clause = list_clause.index(y)
                    del list_clause[index_clause]
    
    return list_clause,assgn_done,assgn

def DPLL(dpll_clauses,dpll_assigned,dpll_assign):
    dpll_sat,dpll_clauses,dpll_assigned,dpll_assign,dpll_done = unit_clause(dpll_clauses,dpll_assigned,dpll_assign)
    
    sacred_assgn = copy.deepcopy(dpll_assign)
    sacred_assgn_done = copy.deepcopy(dpll_assigned)
    sacred_dpll_sat = dpll_sat

    if dpll_done:
        print("DONE")
        return dpll_sat,assgn,assgn_done
        

    if dpll_clauses == [[]] or dpll_clauses ==[]:
        dpll_sat = True
        return dpll_sat,dpll_assign,dpll_assigned
        
    
    elif len(dpll_assigned) == len(inputs):
        dpll_sat = False
       
        return dpll_sat,dpll_assign,dpll_assigned
       
    dummy_clause = copy.deepcopy(dpll_clauses) # Copy
    
    for index in range(0,len(inputs)):
        if not(index in sacred_assgn_done):
            literal = inputs[index]
            literal_bar = literal + "'"

            #True
            dpll_assigned = copy.deepcopy(sacred_assgn_done)
            dpll_assign = copy.deepcopy(sacred_assgn)
            mod_clause = copy.deepcopy(dpll_clauses) # Copy
            
            dpll_assign[index] = True
            dpll_assigned.append(index)
            for clause in dummy_clause:
                index_modclause = mod_clause.index(clause)
                if literal in clause :   
                    del mod_clause[index_modclause]
                if literal_bar in clause :
                    mod_clause[index_modclause].remove(literal_bar)
                
            dpll_sat,dpll_assign,dpll_assigned = DPLL(mod_clause,dpll_assigned,dpll_assign)
            
            if dpll_sat :
                return dpll_sat,dpll_assign,dpll_assigned
            else: 
                 #False
                dpll_assigned = copy.deepcopy(sacred_assgn_done)
                dpll_assign = copy.deepcopy(sacred_assgn)
                mod_clause = copy.deepcopy(dpll_clauses) # Copy
            
                dpll_assign[index] = False
                dpll_assigned.append(index)
                for clause in dummy_clause:
                    index_modclause = mod_clause.index(clause)
                    if literal_bar in clause:   
                        del mod_clause[index_modclause]
                    if literal in clause:
                        mod_clause[index_modclause].remove(literal)
                
                dpll_sat,dpll_assign,dpll_assigned = DPLL(mod_clause,dpll_assigned,dpll_assign)
                if dpll_sat :   
                    return dpll_sat,dpll_assign,dpll_assigned
                
    dpll_done = True
    if dpll_done:
        return dpll_sat,dpll_assign,dpll_assigned
              
def SAT():
    global sat
    if sat :
        print (assgn)
        print(assgn_done)
        print("SAT")
    else:
        print("UNSAT")

sat,list_clause,assgn_done,assgn,done = unit_clause(list_clause,assgn_done,assgn)
if done : 
    SAT()
else:
    list_clause,assgn_done,assgn = pure_literal(list_clause,assgn_done,assgn)
    sat,assgn,assgn_done = DPLL(list_clause,assgn_done,assgn)
    SAT()





