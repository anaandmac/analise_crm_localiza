# Análise CRM Localiza

## Introdução

## Parte 1 - *Churn* de cliente
Primeiro foi feita uma pequena análise exploratória de dados, para entender a base disponibilizada. Após isso, foi feita a verificação a seguinte hipótese:

*“O churn de novos clientes é maior do que o churn de clientes ativos”*

Vamos considerar para *churn* o período de 1 ano. A tabela abaixo mostra a quantidade de contratos abertos e fechados em anos diferentes (coluna **False**) e a quantidade de contratos abertos e fechados no mesmo ano (coluna **True**):

| Ano | False |True|% Mesmo Ano|
| --- | --- |--- | --- |
|2015 |533 |79.633  |99.34|
|2016 |537 |79.298  |99.33|
|2017 |526 |79.503  |99.34|
|2018 |552 |79.645  |99.31|
|2019 |515 |80.001  |99.31|
|2020 |535 |80.001  |99.33|

A quarta coluna (**% Mesmo Ano**) mostra o percentual de clientes que cancelaram o contrato no mesmo ano em que o abriram.

Note que a grande maioria dos contratos são fechados no mesmo ano em que foram celebrados. Logo, dada a hipótese anterior, podemos ver claramente que ela é verdadeira, ou seja, os novos  clientes  tendem mais a cancelar os contratos.

## Parte 2 - Algoritmo de agenda
A segunda tarefa era a criação de um algoritmo que verificasse a disponibilidade de horários de duas pessoas para uma reunião de *t* minutos, dados seus horários de trabalho e suas agendas. O código está no script *Análise CRM.ipynb* deste diretório. Abaixo estão alguns testes feitos e suas saídas:

### Exemplo 1:
`agenda_A=[['9:00','10:30'],['12:00','13:00'],['16:00','18:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=30

horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos)`
- Saída: [['11:30', '12:00'], ['15:00', '16:00'], ['18:00', '18:30']]

### Exemplo 2:

`agenda_A=[['9:00','10:25'],['12:00','13:00'],['16:00','18:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['15:15', '15:40'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=10
`
- Saída: [['11:30', '12:00'], ['15:00', '15:15'], ['15:40', '16:00'], ['18:00', '18:30']]

### Exemplo 3:
`agenda_A=[['9:00','10:00']]
horario_A=['9:00','20:00']

agenda_B=[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['15:15', '15:40'], ['16:00', '17:00']]
horario_B=['10:00','18:30']
tempo_minutos=10

horario_reuniao(agenda_A,horario_A,agenda_B,horario_B,tempo_minutos)`
- Saída: [['11:30', '12:30'], ['15:00', '15:15'], ['15:40', '16:00'], ['17:00', '18:30']]
