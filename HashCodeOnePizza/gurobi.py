# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gurobipy as gp
from gurobipy import GRB
import glob

instances = sorted(glob.glob('input_data/*'))

for inputFile in instances:
    outputFile =  'out_'+ inputFile.split('/')[-1]
    
    f = open(inputFile, "r")
    nCust = int(f.readline())
    
    ingreds = []
    Custs = {}
    
    for i in range(nCust):
        like  = f.readline().split()
    #    if int(like[0])>0:        
        like = set(like[1:int(like[0])+1])
        ingreds.extend(like)
        like = ' '.join(sorted(like))
                
        dlike = f.readline().split()
    #    if int(dlike[0])>0:        
        dlike = set(dlike[1:int(dlike[0])+1])
        dlike = ' '.join(sorted(dlike))
                
        try:
            Custs[like+'*'+dlike] +=1
        except:
            Custs[like+'*'+dlike] =1   
    
    
    Custs.keys()
    ingreds = set(ingreds) 
    nIngreds = len(ingreds)
    
    
    def mycallback(model, where):
    
        if where == GRB.Callback.MIPSOL:
    
            obj = model.cbGet(GRB.Callback.MIPSOL_OBJ)
            
            if obj>model._objBest:
                x = model.cbGetSolution(model._vars)
                val = [model._vars[i].varName for i in range(len(model._vars)) if x[i]==1]
                
                print('')
                print('Solution:', obj)
                print('')
                
         #       print(len(val), ' '.join(val))
                model._objBest = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
                with open(model._outputFile, "w") as file1:
                    file1.write(str(len(val))+' '+' '.join(val))
            
    
    
    model = gp.Model('One Pizza')
    varIngreds = {i: model.addVar(vtype=GRB.BINARY, name=i) for i in ingreds}
    
    varCusts = {i: model.addVar(vtype=GRB.BINARY, name="cust_"+i) for i in Custs.keys()}
        
    
    for k,v in varCusts.items():
        ks = k.split('*')
        like  = ks[0].split()
        dlike = ks[1].split()
        expLike = gp.quicksum([varIngreds[i] for i in like])==len(like)
        expDLike = gp.quicksum([varIngreds[i] for i in dlike if i in varIngreds])==0
        
        model.addConstr((v==1) >> expLike, "constrLike_"+k)
        model.addConstr((v==1) >> expDLike, "constrDLike_"+k)      
        
    
        
    obj = gp.quicksum([Custs[k] * v  for k,v in varCusts.items() ])
    model.setObjective(obj, GRB.MAXIMIZE)
    
    model._vars = list(varIngreds.values())
    model._outputFile = outputFile
    model._objBest = 0
    
    model.optimize(mycallback)
    
    model.write('OnePizza.lp')
    
    
    obj = model.getObjective()
    
    print('')
    print('Solution:', obj.getValue())
    print('')
    
    strIngredFinal = ''
    
    
    val = [v.varName for v in varIngreds.values() if v.X == 1 ]
    
    print(len(val), ' '.join(val))
    
    with open(outputFile, "w") as file1:
        file1.write(str(len(val))+' '+' '.join(val))


