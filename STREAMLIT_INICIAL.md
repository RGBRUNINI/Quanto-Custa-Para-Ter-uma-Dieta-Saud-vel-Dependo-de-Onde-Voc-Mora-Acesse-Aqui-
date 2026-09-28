## README.md — Streamlit (Python) Inicial

A documentação abaixo pode substituir a versão anterior. Os códigos estão comentados e explicados passo a passo, considerando alunos que estão tendo o primeiro contato com Streamlit.

# Streamlit (Python) Inicial

## 1. Objetivo da aula

Nesta aula, vamos aprender a utilizar o **Streamlit**, uma biblioteca Python que permite transformar códigos de análise de dados em uma aplicação web interativa.

A ideia é começar com algo simples:

```text
Python + Pandas
       ↓
Análise dos dados
       ↓
Streamlit
       ↓
Página interativa
```

Durante a aula, será utilizada uma base da **FAO** contendo informações sobre o **Custo de uma Dieta Saudável (CoHD)** em diferentes países e anos.

Ao final da aula, será possível criar uma aplicação na qual o usuário poderá:

* visualizar os dados;
* escolher um país;
* escolher um ano;
* visualizar indicadores;
* consultar uma tabela;
* visualizar gráficos;
* carregar outro arquivo CSV;
* navegar por diferentes áreas da aplicação.

---

# 2. O que é Streamlit?

O Streamlit é uma biblioteca Python utilizada para criar aplicações interativas para dados.

Sem Streamlit, podemos fazer uma análise em Python:

```python
import pandas as pd

df = pd.read_csv("dados.csv")

print(df.head())
```

O resultado aparece apenas no terminal.

Com Streamlit:

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("dados.csv")

st.dataframe(df)
```

A informação passa a ser apresentada em uma página web.

### Comparação

| Python tradicional            | Streamlit                |
| ----------------------------- | ------------------------ |
| `print()`                   | `st.write()`           |
| `print(df)`                 | `st.dataframe(df)`     |
| código executado no terminal | aplicação no navegador |
| interação limitada          | filtros e widgets        |
| análise                      | aplicação interativa   |

---

# 3. Conhecendo a base utilizada

Nesta aula será utilizada a base:

```text
Custo_Dieta_Saudavel_Traduzido_Completo.csv
```

A base possui:

```text
10.320 registros
8 colunas
```

As principais colunas são:

| Coluna           | Tipo    | Explicação             |
| ---------------- | ------- | ------------------------ |
| `Pais_Regiao`  | texto   | País ou região         |
| `Item_Analise` | texto   | Indicador analisado      |
| `Elemento`     | texto   | Elemento da informação |
| `Ano`          | número | Ano do registro          |
| `Publicacao`   | texto   | Publicação relacionada |
| `Unidade`      | texto   | Unidade de medida        |
| `Valor`        | número | Valor do indicador       |
| `Status_Dado`  | texto   | Situação do dado       |

A coluna `Valor` possui alguns valores vazios.

Isso é importante porque, em uma análise real, os dados precisam ser avaliados antes de serem utilizados.

---

# 4. Criando a pasta do projeto

No computador, crie uma pasta chamada:

```text
streamlit_fao
```

Dentro dela teremos:

```text
streamlit_fao
│
├── app.py
├── Custo_Dieta_Saudavel_Traduzido_Completo.csv
└── README.md
```

### O que significa cada arquivo?

### `app.py`

É o programa Python que cria o nosso aplicativo.

### `.csv`

É o arquivo contendo os dados que serão analisados.

### `README.md`

É o arquivo de documentação do projeto.

---

# 5. Abrindo o projeto no VS Code

Abra o VS Code.

Depois selecione:

```text
Arquivo
    ↓
Abrir Pasta
    ↓
streamlit_fao
```

No lado esquerdo do VS Code, deverá aparecer:

```text
EXPLORER

streamlit_fao

    app.py
    Custo_Dieta_Saudavel_Traduzido_Completo.csv
    README.md
```

---

# 6. Abrindo o terminal

No VS Code, selecione:

```text
Terminal
    ↓
Novo Terminal
```

Também podemos utilizar:

```text
Ctrl + `
```

O terminal deverá aparecer na parte inferior do VS Code.

Exemplo:

```powershell
PS C:\Users\Rodrigo\streamlit_fao>
```

---

# 7. Verificando a instalação do Python

Antes de instalar o Streamlit, precisamos verificar se o Python está disponível.

Digite:

```powershell
python --version
```

### O que esse comando faz?

`python`

Indica que queremos utilizar o Python.

`--version`

Solicita que o Python informe sua versão.

Exemplo:

```text
Python 3.14.4
```

Se aparecer a versão do Python, podemos continuar.

---

# 8. Verificando o PIP

O `pip` é uma ferramenta utilizada para instalar bibliotecas Python.

Digite:

```powershell
pip --version
```

Exemplo:

```text
pip 25.x.x
```

Podemos pensar no `pip` como uma espécie de instalador de bibliotecas Python.

---

# 9. Criando um ambiente virtual

Agora vamos criar um ambiente virtual.

Digite:

```powershell
python -m venv .venv
```

### Entendendo o comando

```text
python
```

Executa o Python.

```text
-m
```

Informa que queremos executar um módulo do Python.

```text
venv
```

É o módulo utilizado para criar ambientes virtuais.

```text
.venv
```

É o nome que estamos dando ao ambiente virtual.

Depois do comando, aparecerá uma pasta:

```text
.venv
```

A estrutura ficará:

```text
streamlit_fao
│
├── .venv
├── app.py
├── Custo_Dieta_Saudavel_Traduzido_Completo.csv
└── README.md
```

---

# 10. Ativando o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se funcionar, o terminal deverá mostrar:

```text
(.venv) PS C:\Users\Rodrigo\streamlit_fao>
```

O texto:

```text
(.venv)
```

indica que o ambiente virtual está ativo.

---

# 11. Instalando o Streamlit

Agora vamos instalar o Streamlit.

Digite:

```powershell
pip install streamlit
```

### O que está acontecendo?

O `pip` irá procurar o pacote Streamlit e instalá-lo no ambiente virtual.

Depois da instalação, também vamos instalar as bibliotecas utilizadas na aula:

```powershell
pip install pandas matplotlib plotly
```

Teremos:

```text
Streamlit
    ↓
Criação da aplicação

Pandas
    ↓
Manipulação dos dados

Matplotlib
    ↓
Gráficos

Plotly
    ↓
Gráficos interativos
```

---

# 12. Testando o Streamlit

Para verificar se tudo foi instalado corretamente:

```powershell
streamlit hello
```

O Streamlit abrirá uma aplicação de demonstração.

Caso o navegador não abra automaticamente, procure no terminal algo semelhante a:

```text
Local URL: http://localhost:8501
```

Abra esse endereço no navegador.

---

# 13. Criando o primeiro aplicativo

No VS Code, abra:

```text
app.py
```

Digite:

```python
import streamlit as st

st.title("Custo de uma Dieta Saudável")
```

## Entendendo o código

### Linha 1

```python
import streamlit as st
```

Aqui estamos importando a biblioteca Streamlit.

O trecho:

```python
as st
```

cria um apelido.

Assim, em vez de escrever:

```python
streamlit.title()
```

podemos escrever:

```python
st.title()
```

Isso deixa o código menor e mais fácil de escrever.

---

### Linha 2

```python
st.title("Custo de uma Dieta Saudável")
```

`st` representa o Streamlit.

`title()` cria um título na página.

O texto entre aspas será apresentado para o usuário.

---

# 14. Executando o primeiro aplicativo

No terminal:

```powershell
streamlit run app.py
```

### O que significa?

```text
streamlit
```

Estamos utilizando o Streamlit.

```text
run
```

Significa executar.

```text
app.py
```

É o arquivo Python que contém nossa aplicação.

O resultado será semelhante a:

```text
Local URL: http://localhost:8501
```

Abra o endereço no navegador.

---

# 15. Adicionando texto

Agora vamos acrescentar uma explicação.

```python
import streamlit as st

st.title("Custo de uma Dieta Saudável")

st.write(
    "Aplicação criada com Streamlit utilizando dados da FAO."
)
```

### O que faz `st.write()`?

O comando:

```python
st.write()
```

serve para apresentar informações na tela.

Por exemplo:

```python
st.write("Olá")
```

apresenta:

```text
Olá
```

Também podemos apresentar números:

```python
st.write(100)
```

Ou variáveis:

```python
quantidade = 10320

st.write(quantidade)
```

---

# 16. Carregando os dados

Agora vamos utilizar Pandas.

Adicione:

```python
import streamlit as st
import pandas as pd
```

Depois:

```python
df = pd.read_csv(
    "Custo_Dieta_Saudavel_Traduzido_Completo.csv"
)
```

### Entendendo essa linha

```python
pd.read_csv()
```

é uma função do Pandas utilizada para ler arquivos CSV.

Estamos dizendo:

> "Pandas, leia este arquivo CSV e carregue os dados."

O resultado é armazenado na variável:

```python
df
```

Podemos pensar no `df` como nossa tabela de dados.

---

# 17. Mostrando a tabela

Agora podemos apresentar a tabela:

```python
st.dataframe(df)
```

O código completo:

```python
import streamlit as st
import pandas as pd

df = pd.read_csv(
    "Custo_Dieta_Saudavel_Traduzido_Completo.csv"
)

st.title("Custo de uma Dieta Saudável")

st.dataframe(df)
```

---

# 18. O que é `df`?

Esse é um conceito importante para quem está começando.

`df` é apenas o nome que demos para a tabela.

Poderíamos utilizar:

```python
dados = pd.read_csv(...)
```

ou:

```python
tabela = pd.read_csv(...)
```

ou:

```python
base = pd.read_csv(...)
```

O nome `df` é muito utilizado por profissionais de dados porque é uma abreviação de:

```text
DataFrame
```

Um DataFrame é uma estrutura semelhante a uma tabela.

---

# 19. Mostrando informações da base

Podemos apresentar a quantidade de registros:

```python
st.write(
    "Quantidade de registros:",
    len(df)
)
```

### O que faz `len()`?

`len()` conta a quantidade de elementos.

Nesse caso:

```python
len(df)
```

conta a quantidade de linhas da tabela.

Como nossa base possui 10.320 registros, teremos:

```text
Quantidade de registros: 10320
```

---

# 20. Contando as colunas

Podemos utilizar:

```python
len(df.columns)
```

O código:

```python
st.write(
    "Quantidade de colunas:",
    len(df.columns)
)
```

### Entendendo

```python
df
```

é nossa tabela.

```python
df.columns
```

representa as colunas.

```python
len(df.columns)
```

conta quantas colunas existem.

---

# 21. Exibindo os nomes das colunas

Podemos fazer:

```python
st.write(
    "Colunas:",
    df.columns.tolist()
)
```

O resultado será semelhante a:

```text
Colunas:

Pais_Regiao
Item_Analise
Elemento
Ano
Publicacao
Unidade
Valor
Status_Dado
```

---

# 22. Criando o primeiro Slider

Agora vamos permitir que o usuário escolha um ano.

```python
ano = st.slider(
    "Selecione o ano",
    int(df["Ano"].min()),
    int(df["Ano"].max()),
    int(df["Ano"].max())
)
```

Esse código parece grande, mas podemos entendê-lo por partes.

---

## 22.1 O que é `st.slider()`?

O `slider` cria uma barra que pode ser movimentada.

Por exemplo:

```text
Selecione o ano

2017 ───────────────●──── 2024
```

O usuário pode movimentar o ponto.

---

## 22.2 O que significa `df["Ano"]`?

Estamos selecionando a coluna:

```text
Ano
```

da nossa tabela.

---

## 22.3 O que significa `.min()`?

```python
df["Ano"].min()
```

encontra o menor ano disponível.

---

## 22.4 O que significa `.max()`?

```python
df["Ano"].max()
```

encontra o maior ano disponível.

---

## 22.5 Por que utilizamos `int()`?

```python
int(...)
```

transforma o resultado em número inteiro.

Isso é importante porque o `slider` de anos deve trabalhar com números inteiros.

---

# 23. Filtrando pelo ano

Depois de criar o slider:

```python
df_ano = df[
    df["Ano"] == ano
]
```

### O que estamos fazendo?

Estamos dizendo:

> "Crie uma nova tabela contendo somente os registros cujo ano seja igual ao ano escolhido pelo usuário."

Se o usuário escolher:

```text
2022
```

teremos:

```text
df["Ano"] == 2022
```

---

# 24. Mostrando o resultado do filtro

```python
st.dataframe(df_ano)
```

Assim, a aplicação exibirá somente os registros do ano selecionado.

---

# 25. Criando o Selectbox

Agora vamos permitir que o usuário escolha um país.

```python
pais = st.selectbox(
    "Selecione um país ou região",
    sorted(
        df["Pais_Regiao"]
        .dropna()
        .unique()
    )
)
```

Vamos entender passo a passo.

---

## 25.1 `selectbox`

```python
st.selectbox()
```

cria uma lista de opções.

Exemplo:

```text
Selecione um país

[ Albania ▼ ]
```

Ao clicar, o usuário verá várias opções.

---

## 25.2 `unique()`

```python
df["Pais_Regiao"].unique()
```

retorna os países/regiões sem repetir os valores.

---

## 25.3 `dropna()`

```python
.dropna()
```

remove valores vazios.

---

## 25.4 `sorted()`

```python
sorted(...)
```

organiza as opções em ordem.

---

# 26. Filtrando pelo país

Agora:

```python
df_pais = df[
    df["Pais_Regiao"] == pais
]
```

Estamos criando uma nova tabela contendo somente o país selecionado.

---

# 27. Combinando país e ano

Podemos combinar os dois filtros:

```python
df_filtrado = df[
    (df["Ano"] == ano) &
    (df["Pais_Regiao"] == pais)
]
```

O símbolo:

```python
&
```

significa **E** quando estamos combinando condições em Pandas.

Portanto:

```python
(df["Ano"] == ano)
```

significa:

> O ano é igual ao ano selecionado?

E:

```python
(df["Pais_Regiao"] == pais)
```

significa:

> O país é igual ao país selecionado?

O resultado precisa atender às duas condições.

---

# 28. Criando indicadores com `st.metric()`

Podemos apresentar números importantes no topo da aplicação.

```python
st.metric(
    "Quantidade de registros",
    len(df_filtrado)
)
```

O resultado será semelhante a:

```text
Quantidade de registros

       5
```

---

# 29. Criando três indicadores

Podemos utilizar colunas:

```python
col1, col2, col3 = st.columns(3)
```

Agora:

```python
with col1:
    st.metric(
        "Registros",
        len(df_filtrado)
    )

with col2:
    st.metric(
        "Valor médio",
        f"{df_filtrado['Valor'].mean():.2f}"
    )

with col3:
    st.metric(
        "Valores nulos",
        df_filtrado["Valor"].isna().sum()
    )
```

---

# 30. Entendendo `with`

O comando:

```python
with col1:
```

significa:

> "Tudo que estiver dentro deste bloco será colocado na coluna 1."

Por exemplo:

```python
with col1:
    st.metric("Registros", 100)
```

coloca o indicador na primeira coluna.

---

# 31. Entendendo `mean()`

O comando:

```python
df_filtrado["Valor"].mean()
```

calcula a média.

Exemplo:

```text
Valores:

3
4
5
```

A média é:

```text
(3 + 4 + 5) / 3 = 4
```

---

# 32. Entendendo `isna()`

O comando:

```python
df["Valor"].isna()
```

verifica quais valores estão vazios.

Por exemplo:

```text
Valor

3.20
4.10
vazio
5.20
```

O `isna()` identifica o valor vazio.

Depois:

```python
.sum()
```

conta quantos valores vazios existem.

---

# 33. Criando Tabs

Agora vamos dividir nossa aplicação em três áreas.

```python
tab1, tab2, tab3 = st.tabs(
    [
        "Visão Geral",
        "Gráfico",
        "Dados"
    ]
)
```

Teremos:

```text
┌─────────────────────────────────────────┐
│ Visão Geral | Gráfico | Dados           │
└─────────────────────────────────────────┘
```

---

# 34. Preenchendo a primeira Tab

```python
with tab1:

    st.subheader(
        "Visão Geral"
    )

    st.write(
        "Consulte os principais indicadores da análise."
    )
```

### `st.subheader()`

Cria um subtítulo.

### `st.write()`

Apresenta um texto.

---

# 35. Preenchendo a Tab de dados

```python
with tab3:

    st.subheader(
        "Dados filtrados"
    )

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )
```

O parâmetro:

```python
use_container_width=True
```

faz a tabela utilizar a largura disponível na tela.

---

# 36. Criando gráfico com Matplotlib

Primeiro importamos:

```python
import matplotlib.pyplot as plt
```

Depois podemos criar uma tabela resumida:

```python
media_ano = (
    df.dropna(subset=["Valor"])
      .groupby("Ano")["Valor"]
      .mean()
      .reset_index()
)
```

Essa parte merece atenção.

---

# 37. Entendendo o `groupby()`

Imagine:

```text
Ano    Valor
2020   3.10
2020   3.50
2021   3.20
2021   3.80
```

Se fizermos:

```python
groupby("Ano")
```

estamos dizendo:

> "Agrupe os registros por ano."

Depois:

```python
["Valor"].mean()
```

significa:

> "Calcule a média do valor para cada ano."

Resultado:

```text
Ano    Média
2020   3.30
2021   3.50
```

Esse tipo de operação é muito comum em análise de dados.

---

# 38. Criando o gráfico Matplotlib

```python
fig, ax = plt.subplots()

ax.plot(
    media_ano["Ano"],
    media_ano["Valor"]
)

ax.set_title(
    "Custo médio de uma dieta saudável por ano"
)

ax.set_xlabel("Ano")

ax.set_ylabel("Custo")

st.pyplot(fig)
```

---

# 39. Entendendo o código do gráfico

### Criando a área do gráfico

```python
fig, ax = plt.subplots()
```

Cria uma figura.

Podemos imaginar:

```text
fig
 ↓
┌──────────────────────┐
│                      │
│       gráfico        │
│                      │
└──────────────────────┘
```

---

### Criando a linha

```python
ax.plot(
    media_ano["Ano"],
    media_ano["Valor"]
)
```

O primeiro campo representa o eixo X:

```python
media_ano["Ano"]
```

O segundo representa o eixo Y:

```python
media_ano["Valor"]
```

Portanto:

```text
X = Ano

Y = Valor
```

---

# 40. Exibindo o gráfico no Streamlit

O Matplotlib cria o gráfico.

O Streamlit precisa receber esse gráfico.

Por isso utilizamos:

```python
st.pyplot(fig)
```

Podemos entender:

```text
Matplotlib
     ↓
cria gráfico
     ↓
fig
     ↓
Streamlit
     ↓
st.pyplot(fig)
     ↓
navegador
```

---

# 41. Criando gráfico com Plotly

Primeiro:

```python
import plotly.express as px
```

Agora:

```python
fig = px.line(
    media_ano,
    x="Ano",
    y="Valor",
    markers=True,
    title="Custo médio de uma dieta saudável"
)
```

Depois:

```python
st.plotly_chart(
    fig,
    use_container_width=True
)
```

---

# 42. Por que utilizar Plotly?

Uma das principais vantagens é a interatividade.

O usuário pode:

* passar o mouse sobre os pontos;
* visualizar valores;
* aproximar o gráfico;
* movimentar a visualização;
* interagir com os dados.

Por isso Plotly é muito utilizado em aplicações e dashboards.

---

# 43. Criando um File Uploader

Agora vamos permitir que o usuário carregue seu próprio arquivo.

```python
arquivo = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)
```

O usuário verá algo semelhante a:

```text
Envie um arquivo CSV

[ Browse files ]
```

---

# 44. Verificando se o arquivo foi enviado

Precisamos verificar se existe um arquivo.

```python
if arquivo is not None:

    df_upload = pd.read_csv(
        arquivo
    )

    st.success(
        "Arquivo carregado com sucesso!"
    )

    st.dataframe(
        df_upload
    )
```

---

# 45. Entendendo `if`

O `if` significa:

> "Se uma condição for verdadeira, execute o código."

Neste caso:

```python
if arquivo is not None:
```

significa:

> "Se o usuário enviou um arquivo..."

então:

```python
df_upload = pd.read_csv(arquivo)
```

carrega o arquivo.

---

# 46. Criando um Expander

Podemos esconder informações técnicas utilizando:

```python
with st.expander(
    "Informações técnicas da base"
):

    st.write(
        "Quantidade de registros:",
        len(df)
    )

    st.write(
        "Quantidade de colunas:",
        len(df.columns)
    )

    st.write(
        "Colunas:",
        df.columns.tolist()
    )
```

Na aplicação aparecerá:

```text
▶ Informações técnicas da base
```

Ao clicar:

```text
▼ Informações técnicas da base

Quantidade de registros: 10320

Quantidade de colunas: 8

Colunas:
...
```

---

# 47. Estrutura final da aplicação

A aplicação que estamos construindo terá aproximadamente esta estrutura:

```text
┌─────────────────────────────────────────────┐
│ CUSTO DE UMA DIETA SAUDÁVEL                 │
│                                             │
│ Aplicação utilizando dados da FAO            │
├─────────────────────────────────────────────┤
│ País              │ Ano                     │
│ [Albania ▼]       │ [──────●──────]         │
├─────────────────────────────────────────────┤
│ Registros │ Valor médio │ Valores nulos     │
├─────────────────────────────────────────────┤
│ Visão Geral │ Gráfico │ Dados               │
├─────────────────────────────────────────────┤
│                                             │
│ Conteúdo da análise                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 48. Código completo da primeira aplicação

Depois de compreender cada parte, podemos juntar tudo.

```python
# ==================================================
# 1. BIBLIOTECAS
# ==================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# ==================================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Custo de uma Dieta Saudável",
    layout="wide"
)


# ==================================================
# 3. TÍTULO DA APLICAÇÃO
# ==================================================

st.title(
    "Custo de uma Dieta Saudável"
)

st.write(
    "Aplicação desenvolvida com Streamlit "
    "utilizando dados da FAO."
)


# ==================================================
# 4. CARREGAMENTO DA BASE
# ==================================================

df = pd.read_csv(
    "Custo_Dieta_Saudavel_Traduzido_Completo.csv"
)


# ==================================================
# 5. TRATAMENTO BÁSICO
# ==================================================

# Para os gráficos, vamos utilizar somente
# registros que possuem um valor preenchido.

df_grafico = df.dropna(
    subset=["Valor"]
)


# ==================================================
# 6. FILTRO POR ANO
# ==================================================

ano = st.slider(
    "Selecione o ano",
    int(df["Ano"].min()),
    int(df["Ano"].max()),
    int(df["Ano"].max())
)


# ==================================================
# 7. FILTRO POR PAÍS
# ==================================================

pais = st.selectbox(
    "Selecione o país ou região",
    sorted(
        df["Pais_Regiao"]
        .dropna()
        .unique()
    )
)


# ==================================================
# 8. APLICANDO OS FILTROS
# ==================================================

df_filtrado = df[
    (df["Ano"] == ano) &
    (df["Pais_Regiao"] == pais)
]


# ==================================================
# 9. INDICADORES
# ==================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Registros",
        len(df_filtrado)
    )


with col2:

    st.metric(
        "Valor médio",
        f"{df_filtrado['Valor'].mean():.2f}"
    )


with col3:

    st.metric(
        "Valores nulos",
        df_filtrado["Valor"].isna().sum()
    )


# ==================================================
# 10. ABAS
# ==================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Visão Geral",
        "Gráficos",
        "Dados"
    ]
)


# ==================================================
# 11. ABA VISÃO GERAL
# ==================================================

with tab1:

    st.subheader(
        "Resumo da análise"
    )

    st.write(
        "País/região selecionado:",
        pais
    )

    st.write(
        "Ano selecionado:",
        ano
    )


# ==================================================
# 12. ABA GRÁFICOS
# ==================================================

with tab2:

    st.subheader(
        "Evolução do custo"
    )

    # Seleciona somente o país escolhido
    df_pais = df_grafico[
        df_grafico["Pais_Regiao"] == pais
    ]

    # Calcula a média por ano
    media_ano = (
        df_pais
        .groupby("Ano")["Valor"]
        .mean()
        .reset_index()
    )

    # Cria o gráfico
    fig = px.line(
        media_ano,
        x="Ano",
        y="Valor",
        markers=True,
        title=f"Custo médio — {pais}"
    )

    # Exibe o gráfico
    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==================================================
# 13. ABA DADOS
# ==================================================

with tab3:

    st.subheader(
        "Dados filtrados"
    )

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )


# ==================================================
# 14. EXPANDER
# ==================================================

with st.expander(
    "Informações técnicas da base"
):

    st.write(
        "Quantidade de registros:",
        len(df)
    )

    st.write(
        "Quantidade de colunas:",
        len(df.columns)
    )

    st.write(
        "Colunas disponíveis:",
        df.columns.tolist()
    )


# ==================================================
# 15. UPLOAD DE ARQUIVO
# ==================================================

st.subheader(
    "Carregar outra base"
)

arquivo = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)


if arquivo is not None:

    # Lê o arquivo enviado
    df_upload = pd.read_csv(
        arquivo
    )

    st.success(
        "Arquivo carregado com sucesso!"
    )

    # Mostra os dados enviados
    st.dataframe(
        df_upload,
        use_container_width=True
    )
```

---

# 49. Como executar a aplicação

Sempre que quisermos executar o projeto:

### 1. Abrir o terminal

```text
Terminal → Novo Terminal
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Executar o Streamlit

```powershell
streamlit run app.py
```

### 4. Abrir no navegador

```text
http://localhost:8501
```

---

# 50. O que significa "Deploy local"?

Nesta aula, quando falamos em **deploy local**, não estamos publicando o aplicativo na internet.

Estamos executando o aplicativo no próprio computador.

A sequência é:

```text
Computador
    ↓
Python
    ↓
Streamlit
    ↓
Servidor local
    ↓
Navegador
```

O endereço:

```text
localhost
```

significa que a aplicação está sendo executada no próprio computador.

A porta:

```text
8501
```

é utilizada pelo Streamlit para disponibilizar a aplicação.

---

# 51. Como parar a aplicação

No terminal onde o Streamlit está executando:

```text
Ctrl + C
```

Isso interrompe a execução.

Para executar novamente:

```powershell
streamlit run app.py
```

---

# 52. Uma analogia para facilitar o entendimento

Podemos explicar o Streamlit para um aluno iniciante da seguinte maneira:

### Python

É o profissional que sabe realizar a análise.

### Pandas

É a ferramenta utilizada para organizar e manipular os dados.

### Matplotlib e Plotly

São ferramentas utilizadas para criar gráficos.

### Streamlit

É a ferramenta que coloca tudo isso em uma interface que outras pessoas conseguem utilizar.

```text
              APLICAÇÃO
                  │
              Streamlit
                  │
       ┌──────────┼──────────┐
       │          │          │
     Pandas   Matplotlib   Plotly
       │          │          │
       └──────────┼──────────┘
                  │
                Dados
                  │
                 FAO
```

---

# 53. Exercício prático

## Situação profissional

Imagine que uma equipe de dados recebeu uma nova base contendo informações sobre o custo de uma dieta saudável.

A equipe precisa disponibilizar uma ferramenta simples para que outras pessoas possam explorar os dados.

### Criar uma aplicação contendo:

**1. Título**

```text
Análise do Custo de uma Dieta Saudável
```

**2. Filtros**

* País/região;
* Ano.

**3. Indicadores**

* quantidade de registros;
* valor médio;
* quantidade de valores nulos.

**4. Visualização**

Criar pelo menos:

* 1 gráfico Plotly;
* 1 gráfico Matplotlib.

**5. Organização**

Utilizar:

* colunas;
* tabs;
* expander.

**6. Upload**

Permitir o envio de outro arquivo CSV.

---

# 54. Desafio para os alunos

Depois que a aplicação funcionar, criar uma nova análise:

> Qual foi a evolução do custo médio da dieta saudável ao longo dos anos para o país selecionado?

Para isso, utilizar:

```python
groupby()
```

```python
mean()
```

e um gráfico de linhas.

---

# 55. Checklist final

Ao finalizar a aula, o aluno deverá conseguir:

* [ ] Abrir um projeto no VS Code.
* [ ] Abrir o terminal.
* [ ] Verificar a versão do Python.
* [ ] Utilizar o `pip`.
* [ ] Criar um ambiente virtual.
* [ ] Ativar o ambiente virtual.
* [ ] Instalar o Streamlit.
* [ ] Instalar Pandas.
* [ ] Instalar Matplotlib.
* [ ] Instalar Plotly.
* [ ] Criar um arquivo `app.py`.
* [ ] Importar o Streamlit.
* [ ] Criar um título.
* [ ] Exibir textos.
* [ ] Ler um CSV com Pandas.
* [ ] Exibir uma tabela.
* [ ] Criar um `slider`.
* [ ] Criar um `selectbox`.
* [ ] Criar um `file_uploader`.
* [ ] Criar colunas.
* [ ] Criar um `expander`.
* [ ] Criar `tabs`.
* [ ] Criar indicadores.
* [ ] Criar um gráfico com Matplotlib.
* [ ] Criar um gráfico com Plotly.
* [ ] Filtrar dados.
* [ ] Executar `streamlit run app.py`.
* [ ] Acessar a aplicação pelo navegador.

---

# 56. Resumo dos principais comandos

| Comando                    | O que faz                 |
| -------------------------- | ------------------------- |
| `import streamlit as st` | Importa o Streamlit       |
| `st.title()`             | Cria título              |
| `st.header()`            | Cria título de seção   |
| `st.subheader()`         | Cria subtítulo           |
| `st.write()`             | Exibe informações       |
| `st.dataframe()`         | Exibe uma tabela          |
| `st.metric()`            | Exibe um indicador        |
| `st.slider()`            | Cria controle deslizante  |
| `st.selectbox()`         | Cria lista de seleção   |
| `st.file_uploader()`     | Permite enviar arquivo    |
| `st.columns()`           | Divide a tela em colunas  |
| `st.expander()`          | Cria área expansível    |
| `st.tabs()`              | Cria abas                 |
| `st.pyplot()`            | Exibe gráfico Matplotlib |
| `st.plotly_chart()`      | Exibe gráfico Plotly     |
| `st.success()`           | Exibe mensagem de sucesso |
| `st.set_page_config()`   | Configura a página       |
| `streamlit run app.py`   | Executa a aplicação     |

---

# 57. Fluxo completo aprendido na aula

O aluno deve conseguir visualizar o processo desta maneira:

```text
┌──────────────────────┐
│       DADOS          │
│        FAO           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│       PANDAS         │
│ Ler e tratar dados   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      ANÁLISE         │
│ Filtros e cálculos   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   MATPLOTLIB/PLOTLY  │
│      Gráficos        │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      STREAMLIT       │
│ Interface interativa │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      NAVEGADOR       │
│      Dashboard       │
└──────────────────────┘
```

## Conceito principal

> **Streamlit permite transformar códigos Python de análise de dados em aplicações interativas que podem ser utilizadas diretamente pelo usuário em um navegador.**

A primeira etapa não é criar um dashboard sofisticado. O objetivo é compreender o fluxo:

```text
Dados → Python → Análise → Visualização → Interação
```

Depois que esse fluxo estiver compreendido, novos componentes e recursos podem ser adicionados gradualmente.
