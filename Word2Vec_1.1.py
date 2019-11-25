# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:55:12 2019

@author: Marcus A. Dyhr
"""

#importing needed modules
import gensim, random, numpy as np, pandas as pd, itertools as it


### LOAD AT START OF EACH SESSION ##############

#Loading VADER Sentiment Lexicon
#vader_lex = pd.read_csv('./vader_lexicon_tab.txt', sep="\t", encoding="ISO-8859-1")
#vader_lex.columns = ["token", "mean_sentiment","sd","raw"]
#vader_lex = vader_lex.drop(columns = ["sd", "raw"])

#Load word2vec model (WARNING: LONG LOAD TIME)
#model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

#################################################

############# Load text file ####################

#For each template word slot, there must be a {w_0}, {w_1} etc. or other index for each word.

#txt = f"This is the first word '{w_1}', this is the second '{w_2}' and this is the third '{w_3}'."

#################################################

##Lists of words similar to template words
#murder_sim = model.most_similar('murder', topn = 10)
#fragile_sim = model.most_similar('fragile',topn = 10)
#considerate_sim = model.most_similar('considerate',topn = 10)

#dictionary creation based on VADER

#murder_vader = {}
#for i in murder_sim:
#        if vader_lex["token"].str.contains(i[0]).any():
#            murder_vader[i[0]] = vader_lex.loc[vader_lex['token'] == i[0], 'mean_sentiment'].iloc[0]
#    

#vader_murder = {i[0]: vader_lex.loc[vader_lex['token'] == i[0], 'mean_sentiment'].iloc[0] for i in murder_sim if vader_lex["token"].str.contains(i[0]).any() == True}    

#dictionary comprehension function; creates dict with the sentiment vals of words in list of most similar words in model list
def vader_list(word, number):
    temp_sim = model.most_similar(word, topn = number)
    output_list = [[i[0],vader_lex.loc[vader_lex['token'] == i[0], 'mean_sentiment'].iloc[0]] for i in temp_sim if vader_lex["token"].str.contains(i[0]).any() == True]
    return output_list

#Dictionary creation
murder_dict =[]
murder_dict = vader_list('murder',25)
#inv_murder_dict = {v: k for k, v in murder_dict.items()}

fragile_dict = []
fragile_dict = vader_list('fragile',25)
#inv_fragile_dict = {v: k for k, v in fragile_dict.items()}

considerate_dict = []
considerate_dict = vader_list('invulnerable',25)
#inv_considerate_dict = {v: k for k, v in considerate_dict.items()}


#creating a tuple with each dictionary
combined_dict = (murder_dict, fragile_dict, considerate_dict)

#inv_combined = [inv_murder_dict,inv_fragile_dict,inv_considerate_dict]

### MEAN SEMANTIC VALUE TEXT GENERATOR

def mean_semantic(*word_dicts, mean_val, stepsize = 0.1, prec = 1000):
    prec = prec
    wlist = []
    for wd in word_dicts:
        wlist.append(wd)
    #print(wlist)
    one_list = []
    all_solutions = []
    while prec > 0:
        prec -= 1
        one_list = [random.choice(i) for i in wlist]
        sum = 0
        for i in one_list:
            sum += i[1] 
        list_average = sum/len(one_list)
        #print(list_average)
        if round(list_average,2) in list(np.around(np.arange(mean_val - stepsize,mean_val + stepsize,stepsize/10),2)):
            one_list.sort()
            #print(one_list)
            olist = list(one_list for one_list,_ in it.groupby(one_list))
            all_solutions.append(olist)
##    #create list with all solutions and their mean values
    #print(all_solutions)
    return [all_solutions,list_average]
#    solutions = list(dict.fromkeys(all_solutions))
#    solutions_nm = list(zip(*solutions))[0]
#    print(solutions_nm)
#    allCombs = sorted(all_solutions)
#    combinations = it.product(*(all_solutions[idx] for idx, Numb in enumerate(all_solutions)))
#    print(list(combinations))
#    sol_dict_ord = {i: {h: k for h,k in enumerate(solutions[i][h])}
#        for i,j in enumerate(solutions)}
#    print(sol_dict_ord)
#    sol_dict_ord = {i: {h: k for h,k in enumerate(inv_combined[h][solutions_nm[i][h]])}
#        for i,j in enumerate(solutions_nm)}
#    print(sol_dict_ord)
    #create list with first element in each sublist in solution (= no mean values)
#    solutions_nm = list(zip(*solutions))[0]
#    print(solutions_nm)
#    #create dict with all solutions ordered by number
#    sol_dict = {i: j for i,j in enumerate(solutions_nm)}
#    print(sol_dict)
#    dcount = -1
#    sol_word_dict = {}
     
#    for k in range(0,len(solutions_nm))
#        for n in range(0,len(inv_combined)):
#            sol_word_dict.update([enumerate(enumerate(inv_combined[n][solutions_nm[k][n]]))])
#    for num, sol in enumerate(solutions_nm):
#        sol_word_dict[num] = sol
#        for num2, wval in enumerate(list(sol)):
#            sol[num2] = inv_combined[num2][wval]
#        swd = {i+1: num[inv_combined[i][wval] for i,wval in enumerate(sol)}    
#            
        
        
    #sol_word_dict = {}
    #for nm,sol in sol_dict:
        
        
        
    
murdering = mean_semantic(murder_dict,fragile_dict,considerate_dict,mean_val = -2)



##defining an ordered word list (sentiment scores for each word)
#word1 = tuple(inv_murder_dict.keys())
#word2 = tuple(inv_fragile_dict.keys())
#word3 = tuple(inv_considerate_dict.keys())
##creating a list of the word lists
#word_list = [word1,word2,word3]
##define what average sentiment score we're aiming for
#S = -2
##and the range around the average sentiment score, we're okay with
#step = 0.1
#
#n = 0
#one_lister = []
#all_solutions = []
#while n < 1000:
#    n += 1
#    one_lister = [random.choice(i) for i in word_list]
#    listaverage = sum(one_lister)/len(one_lister)
#    #print(listaverage)
#    if round(listaverage,2) in list(np.around(np.arange(S - step,S + step,step/10),2)):
#        mylist = (tuple(one_lister),listaverage)
#        output_list = tuple(dict.fromkeys(mylist))
#        all_solutions.append(output_list)
#        #print(output_list)
#        
#solutions = list(dict.fromkeys(all_solutions))
##print(solutions)
#
#w1, w2, w3 = str(solutions[1][0][0]), str(solutions[1][0][1]),str(solutions[1][0][2])
#txt = f"This is the first word '{w1}', this is the second '{w2}' and this is the third '{w3}'."
#print(txt)