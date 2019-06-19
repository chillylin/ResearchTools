import scipy as sp
import pandas as pd

# Receive raw data and calculate correlation and p-value 

def correlationtable(data):
    clm = data.columns
    lenth = len(clm)

    corrdf = []
    pvdf = []

    for j in range (0, lenth): 
        correlations = []
        pvalues = []

        for i in range(0, lenth):
            corr, pvalue = sp.stats.pearsonr(data.iloc[:,j], data.iloc[:,i])

            correlations.append(corr)
            pvalues.append(pvalue)

        corrdf.append(pd.DataFrame({clm[j]:correlations},index = clm))
        pvdf.append(pd.DataFrame({clm[j]:pvalues},index = clm))

    return pd.concat(corrdf, axis =1), pd.concat(pvdf, axis =1)
