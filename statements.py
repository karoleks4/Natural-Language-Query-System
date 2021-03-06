# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


# PART A: Processing statements

from nltk.corpus import brown 
br = set(brown.tagged_words())

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self): 
        self.data = {'P':[], 'N':[],'A':[],'I':[],'T':[]}
        
    def add(self,stem,cat):
        if not cat in self.data.keys():
            return "Invalid tag!"
        else:
            self.data[cat].append(stem)
    
    def getAll(self,cat):
        a = set(self.data[cat])
        result = list(a)
        return result;

class FactBase:
    def __init__(self): 
        self.un = {} 
        self.bin = {}
    
    def addUnary(self,pred,e1):
        if not pred in self.un.keys():
            self.un[pred] = [];
        self.un[pred].append(e1)
    
    def queryUnary(self,pred,e1):
        if (pred in self.un.keys()) and (e1 in self.un[pred]):
            return True
        else: 
            return False
    
    def addBinary(self,pred,e1,e2):
        if not pred in self.bin.keys():
            self.bin[pred] = [];
        self.bin[pred].append((e1,e2))
        
    def queryBinary(self,pred,e1,e2):
        if (pred in self.bin.keys()) and ((e1,e2) in self.bin[pred]):
            return True
        else:
            return False

import re 
def verb_stem(s):
    if (next((word for word in br if word == (s, 'VB') or word == (s, 'VBZ')),1) == 1):
        return ""
    else:
        if s == "has":
           s = "have"
        if s == "does":
            s = "do"  
        if re.match('(unt|.)ies', s):
            s = s[:-1]
        elif re.match('.*[^aeiou]ies',s):
            s = s[:-3]
            s = s + 'y'
        elif re.match('.*(o|x|ch|sh|ss|zz)es',s):
            s = s[:-2]
        elif re.match('.*(z|s)es',s):
            s = s[:-1]
        elif re.match('.*[^i]es',s):
            s = s[:-1]
        elif re.match('.*[aeiou]ys', s):
            s = s[:-1]
        elif re.match('.*([^aeiousxyz(ch)(sh)])s',s):
            s = s[:-1]
        return s

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
               
# End of PART A.
