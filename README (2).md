
# Streamlit - Análise de dados do Linkedin

Uma análise de dados utilizando o database analítico obtido no projeto [@ETL-LINKEDIN](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin)





## Como Funciona?

A Pipeline de dados criada no projeto ETL-LINKEDIN envia automaticamente um banco de dados analítico para esse repositório, onde o streamlit está configurado para fazer o deploy.

No arquivo lit.py, é lido um database e os gráficos são montados com base nesses dados.

A estrutura atual seria:
processo ETL >> banco de dados analítico >> visualização e análise com streamlit 
## Documentação técnica

Para o projeto, foi utilizado python, streamlit e o resultado do projeto [@ETL-LINKEDIN](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin)

Ao executar a pipeline, automaticamente o dashboard é atualizado com novos dados obtidos.

Para esse processo, foi utilizada a lib PYGithub, que permite criar commits e pushs em repos do github, só precisando de um token pessoal do Github (Que é possível gerar nas configurações da conta).





## Autores

- [@PedroCozzati](https://www.github.com/PedroCozzati)


## Deploy

Links 

```bash
  Relatório Streamlit: https://relatorios-vagas.streamlit.app/?utm_medium=oembed
```


## Observações

Fique a vontade para sugerir análises com base nos dados obtidos.
## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/PedroCozzati/streamlit-analise-linkedin
```

Instale as dependências

```bash
  pip install -r requirements.txt
```

Rode o comando:

```bash
  streamlit run lit.py
```

Verifique o endereço localhost que é mostrado no terminal

## Stack utilizada

Python, SQL, Pandas, Streamlit, SQLITE


## Screenshots


DAG
![image](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin/assets/80106385/60e6c975-23dc-44a0-a05a-132cd6d6fca7)

Estrutura do projeto
![image](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin/assets/80106385/d476f47a-f4ef-47c5-97d9-473055690f75)

Gráfico utilizando os dados obtidos (MATPLOTLIB)
![image](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin/assets/80106385/bea71478-86a4-43de-929b-45a4f936ff47)
