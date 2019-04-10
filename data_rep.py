import numpy as np
import pandas as pd
from subprocess import check_output
import pdb
from sklearn.cluster import DBSCAN


#Display top symptoms
def disp_common(syd_count, sym):
    
    syd_count=syd_count.sort_values(by='did',ascending=False)
    com_sym=sym['symptom'].loc[syd_count.index].head(30).values
    print('Common Symptoms: \n')
    print(', '.join(com_sym))
    print('\n')

#Create counts table
def create_count(sd_diff):
    for did in did_list:
        temp=[]
        for index,row in sd_diff.iterrows():
            if row['did']==did:
                temp.append(row['syd'])
        
        for syd_1 in temp:
            for syd_2 in temp:
                df_prob[syd_1][syd_2]+=1
    return df_prob

#Load the data from the datasets
def load_data():
    syd=pd.read_csv('input/sym_dis_matrix.csv')
    dia=pd.read_csv('input/dia_t.csv')
    sym=pd.read_csv('input/sym_t.csv')
    diff=pd.read_csv('input/diffsydiw.csv')
    sym_list=np.array(sym['syd'])
    did_list=np.array(dia['did'])

    return syd, dia, sym, diff, sym_list, did_list


#Search the data for the symptom
def query (sym,sym_name):
    sd=sym['symptom'].str.contains(sym_name, regex=False)
    if len(sd[sd==True])==0:
        return []
    
    ind=sd[sd==True].index
    return ind.values


#Return related symptoms
def related (sym_id, df_prob, sym):
    cnt=0
    rel_sym=[]
    sym_count=[]
    for i in range(0,271):
        if (df_prob.loc[sym_id][i]>(df_prob.loc[sym_id].max()/4) and cnt<5):
            if(cnt==0):
                #print('Entered symptom:', sym.loc[sym_id]['symptom'])
                #print('\n')
                print('Related Symptoms:')
            
            rel_sym.append(sym.loc[i]['syd'])
            sym_count.append(df_prob.loc[sym_id][i])
            #print(sym.loc[i]['symptom'])
            cnt+=1
    return rel_sym,sym_count

#Arrange the symptoms according to the count
def order_sym(rel_sym,sym_count):
    data={'syd': rel_sym, 'count':sym_count}
    df=pd.DataFrame(data,columns=['syd','count'])
    df=df.sort_values(by='count',ascending=False)
    return df['syd']

#Print the symptoms according to the count
def order_print(ord_sym,sym,sym_list):
    print('\n')
    for syd in ord_sym:
        ind=np.where(sym_list==syd)
        print(sym['symptom'].loc[ind[0][0]])
    print('\n')


def main():
    #load data into variables
    syd, dia, sym, diff, sym_list, did_list=load_data()
    #convert to lower case
    sym['symptom']=sym['symptom'].map(lambda x: x.lower() if type(x)==str else x)

    #Initialise values
    df_prob=pd.DataFrame(0,index=sym_list, columns=sym_list, dtype=np.int8)
    sd_diff=diff.merge(dia, left_on='did', right_on='did')
    sd_diff=sd_diff.merge(sym, left_on='syd', right_on='syd')
    syd_count=sd_diff[['syd','did']].groupby('syd').count()
    syd_count['id']=range(0,len(syd_count))
    syd_count=syd_count.set_index('id')
    prior_list=np.array(syd_count)
    sd_diff_did=sd_diff.groupby('did')
    #Read the counts table
    df_prob=pd.read_csv('df_prob.csv')

    for i in range(0,271):
        df_prob.iloc[i][i]=0
    
    #Display common symptoms
    disp_common(syd_count, sym)

    #Enter the symptom
    var = input("Enter a symptom:")
    if len(var):
        sym_id=query(sym,var)
    else:
        print("No symptom entered")

    #If any symptom is returned
    if(sym_id.size):
        #If multiple symptoms are returned
        if(len(sym_id))>1:
            print("Did you mean:")
            for id in sym_id:
                print(id, sym['symptom'][id])
                print('\n')
            sym_id= input("Enter the id:")

        rel_sym,sym_count= related(int(sym_id), df_prob,sym)
        ord_sym= order_sym(rel_sym,sym_count)
        order_print(ord_sym,sym,sym_list)


    #If not symptom is returned
    else:
        print('Symptom not found')



if __name__ == "__main__":
    main()



