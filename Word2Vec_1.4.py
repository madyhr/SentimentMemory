# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:55:12 2019

@author: Marcus A. Dyhr
"""
############# MODULES ##########################

import gensim, random, numpy as np, pandas as pd, itertools as it

################################################


### LOAD AT START OF EACH SESSION ##############

#Loading VADER Sentiment Lexicon
#vader_lex = pd.read_csv('./vader_lexicon_tab.txt', sep="\t", encoding="ISO-8859-1")
#vader_lex.columns = ["token", "mean_sentiment","sd","raw"]
#vader_lex = vader_lex.drop(columns = ["sd", "raw"])

#Load word2vec model (WARNING: LONG LOAD TIME)
#model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

#################################################

############# TEXT FILE LOAD ####################

#For each template word slot, there must be a {w_0}, {w_1} etc. or other index for each word.

#txt = f"This is the first word '{w_1}', this is the second '{w_2}' and this is the third '{w_3}'."

#################################################

############# FUNCTIONS #########################

##### List comprehension function; creates list with the sentiment vals of words in list of most similar words in model list = "dictionary"
#'word' is the word, 'number' is the amount of words from 
#the Word2Vec database that should be cross referenced with VADERS (e.g. '25' will return a 8-item list, as |Word2Vec| > |VADERS|)
def vader_list(word, number):
    try: 
        temp_sim = model.most_similar(word, topn = number)
        output_list = [[i[0],vader_lex.loc[vader_lex['token'] == i[0], 'mean_sentiment'].iloc[0]] for i in temp_sim if vader_lex["token"].str.contains(i[0]).any() == True]
        return output_list
    except IndexError as err:
        print("A user-defined word is not in both VADER and the Word2Vec database. Try another word. Error: {}".format(err))


##### Mean semantic value permutation calculator 
#word_dicts = list of word lists
#mean_val = the average sentiment value of the permutation of words you're looking for
#stepsize = range around average you're satisfied with
#prec = how many iterations of the loop that creates permutations, you want to run, higher is more precise
def mean_semantic(word_dicts, mean_val, stepsize = 0.1, prec = 1000):
    prec = prec
    wlist = []
    average_list = []
    for wd in word_dicts:
        wlist.append(wd)
    one_list = []
    all_solutions = []
    #Loop, creates random combinations of words, if their average is close to mean_val, they get added to all_solution list
    while prec > 0:
        prec -= 1
        one_list = [random.choice(i) for i in wlist]
        sum = 0
        for i in one_list:
            sum += i[1] 
        list_average = sum/len(one_list)
        #This is the "around" condition. The range around mean_val is defined by stepsize.
        if round(list_average,2) in list(np.around(np.arange(mean_val - stepsize,mean_val + stepsize,stepsize/10),2)):
            one_list.sort()
            olist = list(one_list for one_list,_ in it.groupby(one_list))
            all_solutions.append([olist,list_average])
    all_solutions = [k for k,v in it.groupby(sorted(all_solutions))]
    #creating seperate list of averages
    average_list = [i[1] for i in all_solutions]
    #removing averages from all_solutions
    for i in all_solutions:
        del(i[1])
        
    return all_solutions, average_list

#################################################

########## WORD "DICTS" #########################

#All the template words in your 

#Word "dictionary" creation
murder_dict = []
murder_dict = vader_list('murder',25)

fragile_dict = []
fragile_dict = vader_list('fragile',25)

considerate_dict = []
considerate_dict = vader_list('invulnerable',25)

maniac_dict = []
maniac_dict = vader_list('angry',25)

#creating a list with each dictionary
combined_dict = [murder_dict, fragile_dict, considerate_dict]

#################################################



#running the function with the combined dicts
murdering = mean_semantic(word_dicts = combined_dict,mean_val = -2, stepsize = 0.05, prec = 1000)

#Using pandas to create a dataframe with the word lists and their averages
data = {'wlist': murdering[0], 'avg': murdering[1]}
df = pd.DataFrame(data)


