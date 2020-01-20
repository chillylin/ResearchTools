import scipy.stats as sp # for spearman correlation
import pandas as pd # for dataframe handling

def sig (pv): # define the rules about converting p-values to significance marks. 
    if not pv:
        return ''    # When  0.10 < p-value
    elif pv < 0.01:
        return '***' # When         p-value < 0.01
    elif pv < 0.05:
        return '**'  # When  0.01 < p-value < 0.05
    elif pv < 0.1:
        return '*'   # When  0.05 < p-value < 0.10
    else:
        return ''    # When encounter error
        
def printspear(datainsert, outpattern):
    spearresult = sp.spearmanr(datainsert)
    correlationdf = pd.DataFrame(spearresult.correlation)
    correlationdf.index = datainsert.columns
    correlationdf.columns = datainsert.columns

    pvaluedf = pd.DataFrame(spearresult.pvalue)
    pvaluedf.index = datainsert.columns
    pvaluedf.columns = datainsert.columns
    
    sigdf = pd.DataFrame()
    for i in pvaluedf:
        sigdf[i] = pvaluedf[i].apply(sig)

    tempdf = pd.DataFrame()
    for i in correlationdf:
        tempdf = pd.concat([tempdf,correlationdf[i],sigdf[i].rename('')], axis =1, sort = False)

    for i in range(len(outpattern)-1):
        for j in range(len(outpattern)-1):
            print (tempdf.iloc[outpattern[i]:outpattern[i+1],outpattern[j]*2:outpattern[(j+1)]*2].to_latex(float_format="{:0.3f}".format))
            
# Usage example
# df must be a dataframe with proper columns' name (will be shown in the final table) and with proper contents (i.e., float or int)
choppingat = [0,6,12,18] # for eaxample, chopping at 0, 6, 12, and 18. 
printspear(df,choppingat) # output the spearman's correlation table. 
