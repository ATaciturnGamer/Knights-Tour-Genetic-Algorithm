#!/usr/bin/env python3
# coding: utf-8


import random



GENE_SIZE = 192
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8



class Induvidual:
    
    def __init__(self):
        self.gene_pool=[]
        for i in range(GENE_SIZE):
            self.gene_pool.append(0)
    def generateGenes(self):
        for i in range(GENE_SIZE):
            self.gene_pool[i] = random.randint(0,1)
    
    def getFitness(self,fn):
        return fn(self.gene_pool)
    
    def crossover(self,mate):
        crossover_point = random.randint(0,191)
        child = Induvidual()
        flag=0
        for i in range(GENE_SIZE):
            if flag==0:
                child.gene_pool[i] = self.gene_pool[i]
                if i==crossover_point:
                    flag = 1
            elif flag==1:
                child.gene_pool[i] = mate.gene_pool[i]
        return child
    
    def mutate(self,mrate):
        if mrate<0 or mrate>1:
            mrate=0
        for i in range(GENE_SIZE):
            x=random.randint(0,100)
            if x<(mrate*100):
                self.gene_pool[i] = 1 if self.gene_pool[i]==0 else 0



class Population:
    
    def __init__(self, fn):
        self.pop_size = 0
        self.induviduals=[]
        self.next_gen=[]
        self.fitness_fn = fn
    
    def initializePop(self, p=10):
        self.pop_size = p
        for i in range(self.pop_size):
            self.induviduals.append(Induvidual())
            self.induviduals[i].generateGenes()
    
    def addInduvidual(self, x):
        self.induviduals.append(x)
        self.pop_size+=1
    def removeInduvidual(self, i):
        self.induviduals.pop(i)
        self.pop_size-=1
    
    def getBestFit(self):
        best_val = 0
        best_index = 0
        for i in range(self.pop_size):
            this_val = self.induviduals[i].getFitness(self.fitness_fn)
            if (this_val>best_val):
                best_val = this_val
                best_index = i
        return self.induviduals[best_index],best_index
            
    
    def tournamentSelection(self, sample_size=3):# 3-Tournament Selection
        if sample_size>self.pop_size:
            sample_size=3
        tour = Population(self.fitness_fn)
        for i in range(sample_size):
            tour.addInduvidual(self.induviduals[random.randint(0,9)])
        par1,i = tour.getBestFit()
        tour.removeInduvidual(i)
        par2,i = tour.getBestFit()
        del tour
        return par1, par2
    
    def breed(self, par1, par2):
        child = par1.crossover(par2)
        child.mutate(MUTATION_RATE)
        return child
    
    def generateNextGeneration(self,elite=1,target=-1):# Generates the (i+1)th generation
        n_size = self.pop_size
        if elite==1:
            n_size-=1
            self.next_gen.append(self.getBestFit()[0])
        for i in range(self.pop_size):
            p1,p2 = self.tournamentSelection()
            if random.randint(0,99)<(CROSSOVER_RATE*100):
                self.next_gen.append(self.breed(p1,p2))
            else:
                p1.mutate(MUTATION_RATE)
                self.next_gen.append(p1)
        self.induviduals = self.next_gen.copy()
        self.next_gen.clear()
        if self.getBestFit()[0].getFitness(self.fitness_fn)==target:
            return True
        return False


class KnightBoard:
    @staticmethod
    def pos2board(pos):
        bpos=[(pos[1]-1),0]
        if pos[0]=="A":
            bpos[1]=0
        elif pos[0]=="B":
            bpos[1]=1
        elif pos[0]=="C":
            bpos[1]=2
        elif pos[0]=="D":
            bpos[1]=3
        elif pos[0]=='E':
            bpos[1]=4
        elif pos[0]=="F":
            bpos[1]=5
        elif pos[0]=="G":
            bpos[1]=6
        elif pos[0]=="H":
            bpos[1]=7
        return bpos
    
    def __init__(self, kpos=["E4"]):
        self.kn_pos = self.pos2board([kpos[0],int(kpos[1])])
        self.ori_pos = self.kn_pos.copy()
        # print("Placed at ", self.pos2board([kpos[0],int(kpos[1])]))
        self.board=[0]*8
        for i in range(8):
            self.board[i] = [0]*8
        self.board[self.kn_pos[0]][self.kn_pos[1]]=1
    
    def reset(self):
        self.kn_pos = self.ori_pos
        for i in range(8):
            self.board[i] = [0]*8
        self.board[self.kn_pos[0]][self.kn_pos[1]]=1
    
    def isVisited(self, pos):
        return self.board[pos[0]][pos[1]]==1
    
    @staticmethod
    def decodeMove(enc_mv):
        return (enc_mv[0]*4+enc_mv[1]*2+enc_mv[2])
    @staticmethod
    def encodeMove(mv):
        if mv==0:
            return [0,0,0]
        elif mv==1:
            return [0,0,1]
        elif mv==2:
            return [0,1,0]
        elif mv==3:
            return [0,1,1]
        elif mv==4:
            return [1,0,0]
        elif mv==5:
            return [1,0,1]
        elif mv==6:
            return [1,1,0]
        elif mv==7:
            return [1,1,1]
    
    def move(self, enc_mv):# Tries to move the knight and returns True if move is valid
        mv = self.decodeMove(enc_mv)
        if mv==0:
            if self.kn_pos[0]>=2 and self.kn_pos[1]<=6:
                if self.isVisited([self.kn_pos[0]-2,self.kn_pos[1]+1]):
                    return False
                self.kn_pos = [self.kn_pos[0]-2,self.kn_pos[1]+1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==1:
            if self.kn_pos[0]>=1 and self.kn_pos[1]<=5:
                if self.isVisited([self.kn_pos[0]-1,self.kn_pos[1]+2]):
                    return False
                self.kn_pos = [self.kn_pos[0]-1,self.kn_pos[1]+2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==2:
            if self.kn_pos[0]<=6 and self.kn_pos[1]<=5:
                if self.isVisited([self.kn_pos[0]+1,self.kn_pos[1]+2]):
                    return False
                self.kn_pos = [self.kn_pos[0]+1,self.kn_pos[1]+2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==3:
            if self.kn_pos[0]<=5 and self.kn_pos[1]<=6:
                if self.isVisited([self.kn_pos[0]+2,self.kn_pos[1]+1]):
                    return False
                self.kn_pos = [self.kn_pos[0]+2,self.kn_pos[1]+1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==4:
            if self.kn_pos[0]<=5 and self.kn_pos[1]>=1:
                if self.isVisited([self.kn_pos[0]+2,self.kn_pos[1]-1]):
                    return False
                self.kn_pos = [self.kn_pos[0]+2,self.kn_pos[1]-1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==5:
            if self.kn_pos[0]<=6 and self.kn_pos[1]>=2:
                if self.isVisited([self.kn_pos[0]+1,self.kn_pos[1]-2]):
                    return False
                self.kn_pos = [self.kn_pos[0]+1,self.kn_pos[1]-2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==6:
            if self.kn_pos[0]>=1 and self.kn_pos[1]>=2:
                if self.isVisited([self.kn_pos[0]-1,self.kn_pos[1]-2]):
                    return False
                self.kn_pos = [self.kn_pos[0]-1,self.kn_pos[1]-2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==7:
            if self.kn_pos[0]>=2 and self.kn_pos[1]>=1:
                if self.isVisited([self.kn_pos[0]-2,self.kn_pos[1]-1]):
                    return False
                self.kn_pos = [self.kn_pos[0]-2,self.kn_pos[1]-1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
    def tryRepair(self,mv_list,index):# Tries to repair current move node.
        ori_mv=self.decodeMove(mv_list[index*3:(index+1)*3])
        for i in range(8):
            if i!=ori_mv:
                enc=self.encodeMove(i)
                if self.move(enc):
                    mv_list[index*3]=enc[0]
                    mv_list[index*3+1]=enc[1]
                    mv_list[index*3+2]=enc[2]
                    return True
        return False
        
    def getValidMoves(self,mv_list):# The fitness function. Evaluates how far the move list gets on the board.
        self.reset()
        num_mvs = len(mv_list)//3
        assert len(mv_list)%3==0
        count = 0
        for i in range(num_mvs):
            if not (self.move(mv_list[i*3:(i+1)*3])):
                if not (self.tryRepair(mv_list,i)):
                    break
            count+=1
        return count
    def showMoves(self,mv_list):# Display all moves on the board in order (0-63).
        self.reset()
        num_mvs = len(mv_list)//3
        assert len(mv_list)%3==0
        mv_arr = [-1]*8
        for i in range(8):
            mv_arr[i] = [-1]*8
        mv_arr[self.kn_pos[0]][self.kn_pos[1]]=0
        for i in range(num_mvs):
            if not (self.move(mv_list[i*3:(i+1)*3])):
                break
            mv_arr[self.kn_pos[0]][self.kn_pos[1]]=i+1
        print("-----Move matrix-----")
        for i in reversed(range(8)):
            print(mv_arr[i])
        return

while True:
	c = input("Enter position of chess knight: (eg: A7) ")
	
	if (c[0].isalpha()) and (c[0].upper()>='A' and c[0].upper()<='H') and (c[1].isdigit()) and (int(c[1])>0 and int(c[1])<9):
		cs = [str(c[0].upper()),int(c[1])]
		break
	print("Try Again")
	

knboard = KnightBoard([cs[0],int(cs[1])])
chb=Population(knboard.getValidMoves)
chb.initializePop(50)


for i in range(2000):
    if i%350==0:
        MUTATION_RATE=0.1
    if i%350==50:
        MUTATION_RATE=0.01
        
    if (chb.generateNextGeneration(1,63)):
        print("Found at Generation: ", i)
        break
    
x,_=chb.getBestFit()
if (x.getFitness(knboard.getValidMoves))!=63:
	print("Could not find path in 2000 generations")
	print("Final fitness: ",x.getFitness(knboard.getValidMoves))
knboard.showMoves(x.gene_pool)


