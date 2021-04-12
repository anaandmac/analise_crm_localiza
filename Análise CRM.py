#!/usr/bin/env python
# coding: utf-8

# # Parte 1

# In[1]:


#Lendo a base
import pandas as pd
base=pd.read_csv('base_teste.csv',index_col='Unnamed: 0')
base.head()


# In[2]:


#Vendo tipo de cada variavel
base.info()


# In[3]:


#Cidade de retirada e de devolucao
retirada_devolucao=pd.pivot_table(base,values='cd_cliente',index=['cidade_retirada'], aggfunc='count').reset_index()
retirada_devolucao=retirada_devolucao.rename(columns={'cidade_retirada':'Cidade','cd_cliente':'Retiradas'})
retirada_devolucao['Devolucao']=(pd.pivot_table(base,values='cd_cliente',index=['cidade_devolucao'], aggfunc='count').reset_index())['cd_cliente']
retirada_devolucao


# In[4]:


import plotly.graph_objects as go

import numpy as np
x0 = np.random.randn(500)
x1 = np.random.randn(500) + 1

fig = go.Figure()
fig.add_trace(go.Histogram(
    x=base['qtd_diarias'],
    histnorm='percent',
    marker_color='slateblue',
    opacity=0.75
))


fig.update_layout(
    title_text='Histograma da quantidade de diárias dos aluguéis',
    xaxis_title_text='Diárias', 
    yaxis_title_text='Frequência',
    plot_bgcolor='rgba(0,0,0,0)',
    bargap=0.2,
    bargroupgap=0.1
)

fig.show()


# In[5]:


#Formato de data e coletando os anos
base['data_abertura_contrato_ano']=base['data_abertura_contrato'].str.split(' ').str[0].str.split('-').str[0]
base['data_abertura_contrato_v2']=pd.to_datetime(base['data_abertura_contrato'].str.split(' ').str[0], format = "%Y-%m-%d" )

base['data_fechamento_contrato_ano']=base['data_fechamento_contrato'].str.split(' ').str[0].str.split('-').str[0]
base['data_fechamento_contrato_v2']=pd.to_datetime(base['data_fechamento_contrato'].str.split(' ').str[0], format = "%Y-%m-%d" )


# In[6]:


#Contratos por ano
contratos_anos=pd.pivot_table(base,values='cd_cliente',index=['data_abertura_contrato_ano'], aggfunc='count').reset_index()
contratos_anos=contratos_anos.rename(columns={'data_abertura_contrato_ano':'Ano','cd_cliente':'Contr. Abertos'})
contratos_anos['Contr. Fechados']=(pd.pivot_table(base,values='cd_cliente',index=['data_fechamento_contrato_ano'], aggfunc='count').reset_index())['cd_cliente']
contratos_anos


# In[7]:


fig = go.Figure()

fig.add_trace(go.Bar(
    x=contratos_anos['Ano'],
    y=contratos_anos['Contr. Abertos'],
    marker_color='steelblue',
    name='Abertos'
))

fig.add_trace(go.Bar(
    x=contratos_anos['Ano'],
    y=contratos_anos['Contr. Fechados'],
    marker_color='turquoise',
    name='Fechados'
))

fig.update_layout(
    title='Quantidade de contratos abertos e fechados por ano',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(
        title='Contratos',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
    title='Ano',
    titlefont_size=16,
    tickfont_size=14,
    )
)
fig.show()


# In[7]:


#Ano de abertura é o mesmo de fechamento?
base['check_ano']=base['data_abertura_contrato_ano']==base['data_fechamento_contrato_ano']
base_cancelamento=pd.pivot_table(base,values='cd_cliente',index=['data_abertura_contrato_ano'],columns=['check_ano'], aggfunc='count')
base_cancelamento['% Mesmo Ano']=round(100*base_cancelamento[True]/(base_cancelamento[False]+base_cancelamento[True]),2)


# A tabela abaixo mostra a quantidade de contratos abertos e fechados em anos diferentes (coluna **False**) e a quantidade de contratos abertos e fechados no mesmo ano (coluna **True**). Note que a grande maioria dos contratos são fechados no mesmo ano em que foram celebrados. 
# 
# Logo, dada a hipótese “*O churn de novos clientes é maior do que o churn de clientes ativos*”, podemos ver claramente que ela é verdadeira.

# In[8]:


base_cancelamento


# # Parte 2

# In[9]:


import datetime
from datetime import timedelta
import numpy as np
import copy

def horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos):
    entrada_A=datetime.datetime.strptime(horario_A[0], '%H:%M')
    saida_A=datetime.datetime.strptime(horario_A[1], '%H:%M')

    entrada_B=datetime.datetime.strptime(horario_B[0], '%H:%M')
    saida_B=datetime.datetime.strptime(horario_B[1], '%H:%M')
    
    inter_inf=max(entrada_A,entrada_B) #quem comeca mais tarde?
    inter_sup=min(saida_A,saida_B) #quem sai mais cedo?
        
    horario_vec=list()
    list_agenda_A_e_B=agenda_A+agenda_B
    agenda_A_e_B=copy.deepcopy(agenda_A)+copy.deepcopy(agenda_B)
    
#     print(agenda_A_e_B)
        #Ajustando as formato de horas de cada agenda
    for a in range(0,len(agenda_A_e_B)):
        agenda_A_e_B[a][0]=datetime.datetime.strptime(agenda_A_e_B[a][0], '%H:%M')
        agenda_A_e_B[a][1]=datetime.datetime.strptime(agenda_A_e_B[a][1], '%H:%M')

    for m in range(0,int((inter_sup-inter_inf).seconds/60),1): # vamos testar passos de 30 min
    #     print(m)
        comeco_reuniao=inter_inf+timedelta(minutes=m)
        final_reuniao=inter_inf+timedelta(minutes=tempo_minutos+m)
        if (final_reuniao<=inter_sup):
            teste_A=list()
            teste_B=list()
            for k in range(0,len(agenda_A_e_B)):
                #reuniao so pode comecar depois de outra
                teste_A=[((comeco_reuniao>agenda_A_e_B[k][0]) and (comeco_reuniao<agenda_A_e_B[k][1])) or
                         ((final_reuniao>agenda_A_e_B[k][0]) and (final_reuniao<agenda_A_e_B[k][1]))]+teste_A
#                 print(teste_A,comeco_reuniao.time().strftime("%H:%M"),final_reuniao.time().strftime("%H:%M"),agenda_A[k][0].time().strftime("%H:%M"),agenda_A[k][1].time().strftime("%H:%M"))
                if(sum(teste_A)==0 and k==len(agenda_A_e_B)-1): #vendo se o comeco esta em um dos intervalos de A
#                     print(comeco_reuniao.time(),agenda_A[k][0].time(),agenda_A[k][1].time())
#                     print(teste_A,comeco_reuniao.time().strftime("%H:%M"),final_reuniao.time().strftime("%H:%M"),agenda_A[k][0].time().strftime("%H:%M"),agenda_A[k][1].time().strftime("%H:%M"))
                      horario=[str(comeco_reuniao.time().strftime("%H:%M"))]+[str(final_reuniao.time().strftime("%H:%M"))]
                      horario_vec=[horario]+horario_vec

    if (len(horario_vec)==0):
        print('Não há horarios disponíveis')
    
    #Ajustando os intervalos
    for k in range(0,len(list_agenda_A_e_B)):
        try:
            horario_vec.remove(list_agenda_A_e_B[k]) #removendo algum intervalo que pode ser de uma reuniao
        except:
            erro=0
        
    horario_vec=sorted(horario_vec, key=lambda x: x[1])#ordenando
    
    list_remove=list()
    #agregando os intervalos "continuos"
    for h in range(0,len(horario_vec)-1):
        if(datetime.datetime.strptime(horario_vec[h][1], '%H:%M')==(datetime.datetime.strptime(horario_vec[h+1][1], '%H:%M')-timedelta(minutes=1))):
    #         print(horario_vec[h][0],horario_vec[h+1][0])
            horario_vec[h+1][0]=horario_vec[h][0]
            list_remove=list_remove+[horario_vec[h]]

    for l in range(0,len(list_remove)):
        horario_vec.remove(list_remove[l])
    

    return(horario_vec)


# In[10]:


#testes
agenda_A=[['9:00','10:30'],['12:00','13:00'],['16:00','18:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=30

horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos)


# In[11]:


agenda_A=[['9:00','10:25'],['12:00','13:00'],['16:00','18:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['15:15', '15:40'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=10

horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos)


# In[13]:


agenda_A=[['9:00','10:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['15:15', '15:40'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=10

horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos)


# In[ ]:




