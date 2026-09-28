# ============================================================
# PROJETO: CUSTO DE UMA DIETA SAUDÁVEL
# ============================================================
#
# DESCRIÇÃO
# ------------------------------------------------------------
# Aplicação interativa desenvolvida em Python utilizando
# Streamlit, Pandas e Plotly.
#
# O objetivo da aplicação é permitir a exploração de dados
# relacionados ao custo de uma dieta saudável em diferentes
# países e regiões ao longo dos anos.
#
# A aplicação permite:
#
#   1. Selecionar um indicador;
#   2. Selecionar até 8 países ou regiões;
#   3. Definir um período de análise;
#   4. Aplicar os filtros por meio de um botão;
#   5. Visualizar KPIs fixos do Brazil;
#   6. Comparar países e regiões no último ano disponível;
#   7. Analisar a evolução temporal dos indicadores;
#   8. Visualizar os dados utilizados na análise;
#   9. Baixar os dados filtrados em CSV;
#  10. Consultar informações gerais da base.
#
#
# ARQUIVO DE DADOS
# ------------------------------------------------------------
# O arquivo CSV deve estar na mesma pasta deste arquivo
# app.py.
#
# Nome esperado:
#
# Custo_Dieta_Saudavel_Traduzido_Completo.csv
#
#
# ESTRUTURA ESPERADA DA BASE
# ------------------------------------------------------------
# A aplicação espera encontrar as seguintes colunas:
#
#   Pais_Regiao
#   Item_Analise
#   Ano
#   Unidade
#   Valor
#   Status_Dado
#   Publicacao
#
#
# REGRAS IMPORTANTES
# ------------------------------------------------------------
#
# 1. Os valores originais da coluna "Unidade" são preservados
#    internamente.
#
# 2. Alguns nomes de unidades recebem apenas um nome amigável
#    para apresentação ao usuário.
#
# 3. Os KPIs do Brazil não dependem dos países selecionados
#    no filtro.
#
# 4. O usuário pode selecionar no máximo 8 países ou regiões.
#
# 5. O filtro somente é aplicado quando o botão
#    "Aplicar filtros" é pressionado.
#
# 6. A evolução temporal é apresentada separadamente para
#    cada unidade encontrada no indicador.
#
# 7. Caso existam mais de duas unidades, apenas as duas
#    primeiras serão utilizadas na visualização.
#
# 8. A "Variação até o maior" representa a variação percentual
#    entre o primeiro valor disponível no período selecionado
#    e o maior valor encontrado nesse mesmo período.
#
# 9. Como estamos analisando custos, o delta dos KPIs utiliza
#    "delta_color='inverse'", de modo que aumentos de custo
#    sejam visualmente tratados como uma variação desfavorável.
#
# ============================================================

# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================
#
# pathlib
#   Permite trabalhar com caminhos de arquivos de maneira
#   independente do sistema operacional.
#
# pandas
#   Utilizado para leitura, tratamento, filtragem e análise
#   dos dados.
#
# plotly.express
#   Utilizado para criação dos gráficos interativos.
#
# streamlit
#   Utilizado para construção da interface web da aplicação.
#
# ============================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ============================================================
#
# st.set_page_config deve ser executado antes dos demais
# elementos visuais da aplicação.
#
# page_title:
#   Define o título exibido na aba do navegador.
#
# page_icon:
#   Define o ícone da aplicação.
#
# layout="wide":
#   Utiliza a largura disponível da tela.
#
# initial_sidebar_state="expanded":
#   Mantém a barra lateral aberta ao iniciar a aplicação.
#
# ============================================================

st.set_page_config(
    page_title="Custo de uma Dieta Saudável",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 3. CONFIGURAÇÃO DOS CAMINHOS
# ============================================================
#
# __file__
#   Representa o caminho do arquivo app.py.
#
# Path(__file__).resolve().parent
#   Identifica a pasta onde o app.py está localizado.
#
# Dessa maneira, o CSV será procurado na mesma pasta do
# aplicativo, evitando depender de caminhos absolutos como:
#
# C:\Users\...
#
# Isso facilita a execução local e também a publicação
# no Streamlit Cloud.
#
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "Custo_Dieta_Saudavel_Traduzido_Completo.csv"
)


# ============================================================
# 4. DICIONÁRIO DE NOMES AMIGÁVEIS
# ============================================================
#
# O banco de dados mantém o nome original da unidade.
#
# Entretanto, nomes técnicos ou muito extensos podem ser
# substituídos por uma descrição mais adequada para o usuário.
#
# IMPORTANTE:
# Essa alteração é somente visual.
#
# O valor original continua sendo utilizado nos filtros,
# cálculos e análises.
#
# ============================================================

NOMES_UNIDADES = {

    "Int$ (Paridade do Poder de Compra) por pessoa por dia":
        "Paridade do Poder de Compra (Pessoa/dia)"

}


# ============================================================
# 5. FUNÇÃO — NOME AMIGÁVEL DA UNIDADE
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Converter o nome técnico da unidade em um nome mais amigável
# para apresentação na interface.
#
# PARÂMETRO
# ------------------------------------------------------------
# unidade:
#   Nome original da unidade presente na base.
#
# RETORNO
# ------------------------------------------------------------
# Retorna o nome amigável quando existir no dicionário.
# Caso contrário, retorna o próprio nome original.
#
# ============================================================

def nome_unidade_exibicao(unidade):

    return NOMES_UNIDADES.get(
        unidade,
        unidade
    )


# ============================================================
# 6. FUNÇÃO — CARREGAMENTO DA BASE
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Ler o arquivo CSV, validar sua estrutura e converter os
# campos necessários para tipos apropriados.
#
# CACHE
# ------------------------------------------------------------
# @st.cache_data permite que o resultado do carregamento seja
# reutilizado em novas execuções quando os parâmetros forem
# iguais.
#
# Isso evita ler e processar novamente o CSV em toda interação
# da aplicação.
#
# A documentação oficial do Streamlit recomenda st.cache_data
# para funções que retornam dados, como DataFrames.
#
# ENTRADA
# ------------------------------------------------------------
# caminho:
#   Caminho do arquivo CSV.
#
# SAÍDA
# ------------------------------------------------------------
# DataFrame contendo os dados tratados.
#
# VALIDAÇÕES
# ------------------------------------------------------------
# A função verifica se todas as colunas obrigatórias existem.
#
# ============================================================

@st.cache_data(show_spinner=False)
def carregar_dados(caminho: Path) -> pd.DataFrame:

    """
    Carrega e prepara a base de dados.

    Etapas realizadas:
        1. Leitura do CSV;
        2. Validação das colunas obrigatórias;
        3. Conversão do campo Ano;
        4. Conversão do campo Valor;
        5. Remoção de registros sem ano.
    """

    # --------------------------------------------------------
    # Leitura do arquivo
    # --------------------------------------------------------

    dados = pd.read_csv(caminho)

    # --------------------------------------------------------
    # Definição das colunas obrigatórias
    # --------------------------------------------------------

    colunas_esperadas = {
        "Pais_Regiao",
        "Item_Analise",
        "Ano",
        "Unidade",
        "Valor",
        "Status_Dado",
        "Publicacao",
    }

    # --------------------------------------------------------
    # Identificação de colunas ausentes
    # --------------------------------------------------------

    ausentes = colunas_esperadas.difference(
        dados.columns
    )

    # --------------------------------------------------------
    # Interrompe a execução caso a estrutura da base esteja
    # incorreta.
    # --------------------------------------------------------

    if ausentes:

        raise ValueError(
            "O CSV não contém as colunas obrigatórias: "
            + ", ".join(sorted(ausentes))
        )

    # --------------------------------------------------------
    # Conversão do ano
    #
    # errors="coerce" transforma valores inválidos em NA.
    # Int64 permite manter valores ausentes em uma coluna
    # inteira.
    # --------------------------------------------------------

    dados["Ano"] = pd.to_numeric(
        dados["Ano"],
        errors="coerce"
    ).astype("Int64")

    # --------------------------------------------------------
    # Conversão dos valores numéricos
    # --------------------------------------------------------

    dados["Valor"] = pd.to_numeric(
        dados["Valor"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Registros sem ano não podem participar de uma análise
    # temporal.
    # --------------------------------------------------------

    dados = dados.dropna(
        subset=["Ano"]
    )

    return dados


# ============================================================
# 7. FUNÇÃO — FORMATAÇÃO DE VALORES
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Transformar valores numéricos em textos adequados para
# apresentação ao usuário.
#
# EXEMPLOS
# ------------------------------------------------------------
# 1234.56
#     1.234,56
#
# 12.5 quando unidade for %
#     12,5%
#
# ============================================================

def formatar_valor(
    valor: float,
    unidade: str
) -> str:

    # --------------------------------------------------------
    # Tratamento de valores ausentes
    # --------------------------------------------------------

    if pd.isna(valor):

        return "—"

    # --------------------------------------------------------
    # Tratamento de percentuais
    # --------------------------------------------------------

    if unidade == "%":

        return (
            f"{valor:,.1f}%"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # --------------------------------------------------------
    # Formatação numérica padrão brasileira
    # --------------------------------------------------------

    texto = (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    # --------------------------------------------------------
    # Caso a unidade represente milhões, adiciona "mi".
    # --------------------------------------------------------

    if "milhões" in unidade.lower():

        texto += " mi"

    return texto


# ============================================================
# 8. FUNÇÃO — CÁLCULO DE VARIAÇÃO PERCENTUAL
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Calcular quanto um valor aumentou ou diminuiu em relação
# a outro valor.
#
# FÓRMULA
# ------------------------------------------------------------
#
#       valor_final - valor_inicial
# V% = ----------------------------- × 100
#             valor_inicial
#
# No dashboard:
#
# valor_inicial = primeiro valor disponível no período
# valor_final   = maior valor encontrado no período
#
# ============================================================

def calcular_variacao_percentual(
    valor_inicial,
    valor_final
):

    # --------------------------------------------------------
    # Não é possível calcular se algum valor estiver ausente.
    # --------------------------------------------------------

    if pd.isna(valor_inicial):

        return None

    if pd.isna(valor_final):

        return None

    # --------------------------------------------------------
    # Evita divisão por zero.
    # --------------------------------------------------------

    if valor_inicial == 0:

        return None

    # --------------------------------------------------------
    # Cálculo da variação percentual
    # --------------------------------------------------------

    return (
        (valor_final - valor_inicial)
        / valor_inicial
    ) * 100


# ============================================================
# 9. FUNÇÃO — GRÁFICO DE EVOLUÇÃO
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Criar um gráfico de linhas mostrando a evolução dos valores
# ao longo dos anos.
#
# CADA LINHA
# ------------------------------------------------------------
# Representa um país ou região.
#
# EIXO X
# ------------------------------------------------------------
# Ano.
#
# EIXO Y
# ------------------------------------------------------------
# Valor do indicador.
#
# ============================================================

def criar_grafico_evolucao(
    dados: pd.DataFrame,
    unidade: str,
    titulo: str,
):

    # --------------------------------------------------------
    # Filtra somente a unidade solicitada.
    # --------------------------------------------------------

    dados_grafico = (
        dados[
            dados["Unidade"] == unidade
        ]
        .sort_values(
            [
                "Pais_Regiao",
                "Ano"
            ]
        )
    )

    # --------------------------------------------------------
    # Nome amigável da unidade.
    # --------------------------------------------------------

    unidade_exibicao = (
        nome_unidade_exibicao(
            unidade
        )
    )

    # --------------------------------------------------------
    # Criação do gráfico.
    # --------------------------------------------------------

    figura = px.line(
        dados_grafico,
        x="Ano",
        y="Valor",
        color="Pais_Regiao",
        markers=True,
        labels={
            "Ano": "Ano",
            "Valor": unidade_exibicao,
            "Pais_Regiao": "País / região",
        },
        title=titulo,
    )

    # --------------------------------------------------------
    # Configurações visuais.
    # --------------------------------------------------------

    figura.update_layout(
        hovermode="x unified",
        legend_title_text="País / região",
        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20,
        ),
    )

    # --------------------------------------------------------
    # Mostra todos os anos disponíveis no eixo X.
    # --------------------------------------------------------

    figura.update_xaxes(
        dtick=1
    )

    # --------------------------------------------------------
    # Configuração do tooltip.
    # --------------------------------------------------------

    figura.update_traces(
        hovertemplate=(
            "%{y:,.2f}"
            "<extra></extra>"
        )
    )

    return figura


# ============================================================
# 10. FUNÇÃO — GRÁFICO COMPARATIVO
# ============================================================
#
# OBJETIVO
# ------------------------------------------------------------
# Comparar os países ou regiões selecionados em um determinado
# ano.
#
# TIPO DE GRÁFICO
# ------------------------------------------------------------
# Barras horizontais.
#
# Cada barra representa um país ou região.
#
# Os valores são ordenados do menor para o maior.
#
# ============================================================

def criar_grafico_comparativo(
    dados: pd.DataFrame,
    unidade: str,
    ultimo_ano: int,
):

    # --------------------------------------------------------
    # Seleciona a unidade e o último ano.
    # --------------------------------------------------------

    dados_comparacao = dados[
        (dados["Unidade"] == unidade)
        &
        (dados["Ano"] == ultimo_ano)
    ].copy()

    # --------------------------------------------------------
    # Ordenação crescente.
    # --------------------------------------------------------

    dados_comparacao = (
        dados_comparacao
        .sort_values(
            "Valor",
            ascending=True
        )
    )

    # --------------------------------------------------------
    # Nome amigável.
    # --------------------------------------------------------

    unidade_exibicao = (
        nome_unidade_exibicao(
            unidade
        )
    )

    # --------------------------------------------------------
    # Criação do gráfico.
    # --------------------------------------------------------

    figura = px.bar(
        dados_comparacao,
        x="Valor",
        y="Pais_Regiao",
        orientation="h",
        text="Valor",
        labels={
            "Valor": unidade_exibicao,
            "Pais_Regiao": "",
        },
        title=(
            f"Comparação entre países — "
            f"{ultimo_ano}"
        ),
    )

    # --------------------------------------------------------
    # Configuração dos valores exibidos nas barras.
    # --------------------------------------------------------

    figura.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        hovertemplate=(
            "%{y}<br>"
            "Valor: %{x:,.2f}"
            "<extra></extra>"
        ),
    )

    # --------------------------------------------------------
    # Configurações visuais.
    # --------------------------------------------------------

    figura.update_layout(
        margin=dict(
            l=20,
            r=60,
            t=70,
            b=20,
        ),
        showlegend=False,
        yaxis={
            "categoryorder": "total ascending"
        },
    )

    return figura


# ============================================================
# 11. CARREGAMENTO DA BASE
# ============================================================
#
# Aqui a aplicação executa a função de carregamento.
#
# São tratados erros comuns:
#
# FileNotFoundError
#   Arquivo CSV não encontrado.
#
# ParserError
#   Problema estrutural no CSV.
#
# UnicodeDecodeError
#   Problema relacionado à codificação do arquivo.
#
# ValueError
#   Estrutura da base incompatível com o esperado.
#
# ============================================================

try:

    df = carregar_dados(
        DATA_FILE
    )

except FileNotFoundError:

    st.error(
        "Não foi possível encontrar o arquivo CSV."
    )

    st.code(
        "Custo_Dieta_Saudavel_Traduzido_Completo.csv"
    )

    st.stop()

except (
    pd.errors.ParserError,
    UnicodeDecodeError,
    ValueError,
) as erro:

    st.error(
        f"Não foi possível carregar a base de dados: {erro}"
    )

    st.stop()


# ============================================================
# 12. CABEÇALHO DA APLICAÇÃO
# ============================================================

st.title(
    "🥗 Custo de uma Dieta Saudável"
)

st.markdown(
    """
    Explore a evolução do custo de uma dieta saudável
    e compare diferentes países ou regiões ao longo do tempo.
    """
)

st.caption(
    "Aplicação desenvolvida com Python, Pandas, Plotly e Streamlit."
)

st.divider()


# ============================================================
# 13. PREPARAÇÃO DOS INDICADORES
# ============================================================
#
# Obtém os indicadores disponíveis na base.
#
# dropna()
#   Remove valores ausentes.
#
# unique()
#   Retorna os valores distintos.
#
# sorted()
#   Organiza alfabeticamente.
#
# ============================================================

itens = sorted(
    df[
        "Item_Analise"
    ]
    .dropna()
    .unique()
)


# ============================================================
# 14. INDICADOR PADRÃO
# ============================================================
#
# Define qual indicador será selecionado automaticamente
# quando a aplicação for aberta.
#
# ============================================================

item_padrao = (
    "Custo de uma dieta saudável (CoHD)"
)


if item_padrao in itens:

    indice_padrao = itens.index(
        item_padrao
    )

else:

    indice_padrao = 0


# ============================================================
# 15. BARRA LATERAL — FILTROS
# ============================================================
#
# Os filtros ficam dentro de st.form.
#
# DIFERENÇA IMPORTANTE
# ------------------------------------------------------------
# Normalmente, cada interação com um widget provoca uma nova
# execução do script.
#
# Ao utilizar st.form, os widgets ficam agrupados e seus
# valores são enviados juntos quando o usuário pressiona
# "Aplicar filtros".
#
# Isso torna a experiência mais adequada para um dashboard
# com múltiplos filtros.
#
# ============================================================

with st.sidebar:

    st.header(
        "🎛️ Filtros"
    )

    st.divider()

    with st.form(
        "formulario_filtros",
        clear_on_submit=False
    ):

        # ====================================================
        # 15.1 — INDICADOR
        # ====================================================

        st.subheader(
            "Indicador"
        )

        item = st.selectbox(
            "Selecione o indicador",
            itens,
            index=indice_padrao,
        )

        # ====================================================
        # 15.2 — BASE DO INDICADOR
        # ====================================================
        #
        # Todos os filtros seguintes dependem do indicador
        # selecionado.
        #
        # ====================================================

        base_indicador_filtro = df[
            df["Item_Analise"] == item
        ].copy()

        # ====================================================
        # 15.3 — PAÍSES / REGIÕES
        # ====================================================

        paises_disponiveis = sorted(
            base_indicador_filtro[
                "Pais_Regiao"
            ]
            .dropna()
            .unique()
        )

        # ----------------------------------------------------
        # Tenta selecionar Brazil e World automaticamente.
        # ----------------------------------------------------

        selecao_padrao = [
            pais
            for pais in (
                "Brazil",
                "World"
            )
            if pais in paises_disponiveis
        ]

        # ----------------------------------------------------
        # Caso Brazil e World não existam, seleciona o primeiro
        # país disponível.
        # ----------------------------------------------------

        if (
            not selecao_padrao
            and paises_disponiveis
        ):

            selecao_padrao = [
                paises_disponiveis[0]
            ]

        # ----------------------------------------------------
        # Permite no máximo 8 países ou regiões.
        # ----------------------------------------------------

        paises = st.multiselect(
            "Países ou regiões",
            paises_disponiveis,
            default=selecao_padrao,
            max_selections=8,
            placeholder="Selecione até 8 opções",
        )

        # ====================================================
        # 15.4 — PERÍODO
        # ====================================================

        if base_indicador_filtro.empty:

            st.warning(
                "Não existem dados para o indicador selecionado."
            )

            st.stop()

        # ----------------------------------------------------
        # Ano inicial disponível.
        # ----------------------------------------------------

        ano_minimo = int(
            base_indicador_filtro[
                "Ano"
            ].min()
        )

        # ----------------------------------------------------
        # Ano final disponível.
        # ----------------------------------------------------

        ano_maximo = int(
            base_indicador_filtro[
                "Ano"
            ].max()
        )

        # ----------------------------------------------------
        # Seleção do intervalo.
        # ----------------------------------------------------

        intervalo = st.slider(
            "Período",
            min_value=ano_minimo,
            max_value=ano_maximo,
            value=(
                ano_minimo,
                ano_maximo
            ),
        )

        # ====================================================
        # 15.5 — BOTÃO DE APLICAÇÃO
        # ====================================================
        #
        # Este botão envia os valores dos widgets presentes
        # no formulário para a aplicação.
        #
        # ====================================================

        aplicar_filtros = st.form_submit_button(
            "🔎 Aplicar filtros",
            type="primary",
            width="stretch",
        )

    # ========================================================
    # 15.6 — SEÇÃO SOBRE
    # ========================================================

    st.divider()

    st.subheader(
        "ℹ️ Sobre"
    )

    st.write(
        """
        Esta aplicação permite explorar indicadores
        relacionados ao custo de uma dieta saudável
        ao longo do tempo.
        """
    )

    st.caption(
        "Dados organizados para fins de exploração e análise."
    )


# ============================================================
# 16. VALIDAÇÃO DA SELEÇÃO DE PAÍSES
# ============================================================
#
# Pelo menos um país ou região precisa ser selecionado.
#
# ============================================================

if not paises:

    st.info(
        "Selecione pelo menos um país ou região "
        "na barra lateral e clique em "
        "'Aplicar filtros'."
    )

    st.stop()


# ============================================================
# 17. FILTRAGEM PRINCIPAL
# ============================================================
#
# Aplica os critérios selecionados:
#
#   - países/regiões;
#   - ano inicial;
#   - ano final.
#
# Também são removidos registros sem Valor.
#
# ============================================================

filtrado = base_indicador_filtro[
    base_indicador_filtro[
        "Pais_Regiao"
    ].isin(paises)
    &
    base_indicador_filtro[
        "Ano"
    ].between(
        intervalo[0],
        intervalo[1]
    )
].dropna(
    subset=["Valor"]
).copy()


# ============================================================
# 18. VALIDAÇÃO DO RESULTADO DO FILTRO
# ============================================================

if filtrado.empty:

    st.warning(
        "Não há valores disponíveis "
        "para os filtros selecionados."
    )

    st.stop()


# ============================================================
# 19. IDENTIFICAÇÃO DAS UNIDADES
# ============================================================
#
# Um mesmo indicador pode possuir mais de uma unidade.
#
# A aplicação foi estruturada para apresentar duas unidades.
#
# ============================================================

unidades = sorted(
    filtrado[
        "Unidade"
    ]
    .dropna()
    .unique()
)


# ------------------------------------------------------------
# É necessário ter pelo menos duas unidades para a estrutura
# atual do dashboard.
# ------------------------------------------------------------

if len(unidades) < 2:

    st.warning(
        "O indicador selecionado possui menos de duas "
        "unidades disponíveis."
    )

    st.stop()


# ------------------------------------------------------------
# Caso existam mais de duas unidades, a aplicação utiliza
# somente as duas primeiras.
# ------------------------------------------------------------

if len(unidades) > 2:

    st.warning(
        "O indicador selecionado possui mais de duas "
        "unidades. Serão utilizadas as duas primeiras."
    )

    unidades = unidades[:2]


unidade_1 = unidades[0]

unidade_2 = unidades[1]


# ============================================================
# 20. NOMES DAS UNIDADES PARA EXIBIÇÃO
# ============================================================

unidade_1_exibicao = (
    nome_unidade_exibicao(
        unidade_1
    )
)

unidade_2_exibicao = (
    nome_unidade_exibicao(
        unidade_2
    )
)


# ============================================================
# 21. IDENTIFICAÇÃO DO ÚLTIMO ANO
# ============================================================
#
# O último ano é calculado com base nos dados filtrados.
#
# Isso significa que o gráfico comparativo sempre utilizará
# o último ano disponível dentro do período selecionado.
#
# ============================================================

ultimo_ano = int(
    filtrado[
        "Ano"
    ].max()
)


# ============================================================
# 22. SEÇÃO DE KPIs DO BRAZIL
# ============================================================
#
# IMPORTANTE:
#
# Os KPIs do Brazil são calculados separadamente dos países
# selecionados.
#
# Assim, selecionar outro conjunto de países não altera
# a referência dos KPIs.
#
# O período selecionado, entretanto, continua sendo aplicado.
#
# ============================================================

st.subheader(
    "🇧🇷 Indicadores do Brazil"
)

st.caption(
    "Os indicadores abaixo permanecem fixos em Brazil, "
    "independentemente dos países selecionados."
)


# ============================================================
# 23. DADOS DO BRAZIL
# ============================================================
#
# Filtra somente:
#
#   Pais_Regiao = Brazil
#
# e mantém o período escolhido pelo usuário.
#
# ============================================================

dados_brazil = base_indicador_filtro[
    base_indicador_filtro[
        "Pais_Regiao"
    ].eq("Brazil")
    &
    base_indicador_filtro[
        "Ano"
    ].between(
        intervalo[0],
        intervalo[1]
    )
].dropna(
    subset=["Valor"]
).copy()


# ============================================================
# 24. VALIDAÇÃO DOS DADOS DO BRAZIL
# ============================================================

if dados_brazil.empty:

    st.warning(
        "Não foram encontrados dados do Brazil "
        "para o período selecionado."
    )

else:

    # ========================================================
    # 25. KPIs — UNIDADE 1
    # ========================================================

    st.markdown(
        f"**{unidade_1_exibicao}**"
    )

    # --------------------------------------------------------
    # Filtra somente a primeira unidade.
    # --------------------------------------------------------

    brazil_unidade_1 = dados_brazil[
        dados_brazil[
            "Unidade"
        ] == unidade_1
    ]

    if not brazil_unidade_1.empty:

        # ----------------------------------------------------
        # Último ano disponível.
        # ----------------------------------------------------

        ultimo_ano_brasil_1 = int(
            brazil_unidade_1[
                "Ano"
            ].max()
        )

        # ----------------------------------------------------
        # Registro correspondente ao último ano.
        # ----------------------------------------------------

        brasil_ano_1 = (
            brazil_unidade_1[
                brazil_unidade_1[
                    "Ano"
                ] == ultimo_ano_brasil_1
            ]
            .sort_values("Ano")
        )

        valor_brasil_1 = (
            brasil_ano_1[
                "Valor"
            ].iloc[0]
        )

        # ----------------------------------------------------
        # Primeiro valor disponível no período.
        # ----------------------------------------------------

        primeiro_valor_brasil_1 = (
            brazil_unidade_1
            .sort_values("Ano")
            ["Valor"]
            .iloc[0]
        )

        # ----------------------------------------------------
        # Menor valor encontrado.
        # ----------------------------------------------------

        minimo_brasil_1 = (
            brazil_unidade_1[
                "Valor"
            ].min()
        )

        # ----------------------------------------------------
        # Maior valor encontrado.
        # ----------------------------------------------------

        maximo_brasil_1 = (
            brazil_unidade_1[
                "Valor"
            ].max()
        )

        # ----------------------------------------------------
        # Variação entre o primeiro valor e o maior valor.
        # ----------------------------------------------------

        variacao_maximo_brasil_1 = (
            calcular_variacao_percentual(
                primeiro_valor_brasil_1,
                maximo_brasil_1
            )
        )

        # ----------------------------------------------------
        # Criação das cinco colunas de KPI.
        # ----------------------------------------------------

        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        # ----------------------------------------------------
        # KPI 1 — Último ano
        # ----------------------------------------------------

        with col1:

            st.metric(
                "📅 Último ano",
                ultimo_ano_brasil_1
            )

        # ----------------------------------------------------
        # KPI 2 — Último valor
        # ----------------------------------------------------

        with col2:

            st.metric(
                "🇧🇷 Último valor",
                formatar_valor(
                    valor_brasil_1,
                    unidade_1
                )
            )

        # ----------------------------------------------------
        # KPI 3 — Menor valor
        # ----------------------------------------------------

        with col3:

            st.metric(
                "⬇️ Menor valor",
                formatar_valor(
                    minimo_brasil_1,
                    unidade_1
                )
            )

        # ----------------------------------------------------
        # KPI 4 — Maior valor
        # ----------------------------------------------------

        with col4:

            st.metric(
                "⬆️ Maior valor",
                formatar_valor(
                    maximo_brasil_1,
                    unidade_1
                )
            )

        # ----------------------------------------------------
        # KPI 5 — Variação até o maior
        # ----------------------------------------------------

        with col5:

            if variacao_maximo_brasil_1 is not None:

                st.metric(
                    "📈 Variação até o maior",
                    f"{variacao_maximo_brasil_1:.1f}%",
                    delta=f"{variacao_maximo_brasil_1:.1f}%",
                    delta_color="inverse"
                )

            else:

                st.metric(
                    "📈 Variação até o maior",
                    "—"
                )


    # ========================================================
    # 26. KPIs — UNIDADE 2
    # ========================================================

    st.markdown(
        f"**{unidade_2_exibicao}**"
    )

    # --------------------------------------------------------
    # Filtra somente a segunda unidade.
    # --------------------------------------------------------

    brazil_unidade_2 = dados_brazil[
        dados_brazil[
            "Unidade"
        ] == unidade_2
    ]

    if not brazil_unidade_2.empty:

        # ----------------------------------------------------
        # Último ano disponível.
        # ----------------------------------------------------

        ultimo_ano_brasil_2 = int(
            brazil_unidade_2[
                "Ano"
            ].max()
        )

        # ----------------------------------------------------
        # Registro correspondente ao último ano.
        # ----------------------------------------------------

        brasil_ano_2 = (
            brazil_unidade_2[
                brazil_unidade_2[
                    "Ano"
                ] == ultimo_ano_brasil_2
            ]
            .sort_values("Ano")
        )

        valor_brasil_2 = (
            brasil_ano_2[
                "Valor"
            ].iloc[0]
        )

        # ----------------------------------------------------
        # Primeiro valor disponível no período.
        # ----------------------------------------------------

        primeiro_valor_brasil_2 = (
            brazil_unidade_2
            .sort_values("Ano")
            ["Valor"]
            .iloc[0]
        )

        # ----------------------------------------------------
        # Menor valor encontrado.
        # ----------------------------------------------------

        minimo_brasil_2 = (
            brazil_unidade_2[
                "Valor"
            ].min()
        )

        # ----------------------------------------------------
        # Maior valor encontrado.
        # ----------------------------------------------------

        maximo_brasil_2 = (
            brazil_unidade_2[
                "Valor"
            ].max()
        )

        # ----------------------------------------------------
        # Variação entre o primeiro valor e o maior valor.
        # ----------------------------------------------------

        variacao_maximo_brasil_2 = (
            calcular_variacao_percentual(
                primeiro_valor_brasil_2,
                maximo_brasil_2
            )
        )

        # ----------------------------------------------------
        # Cinco KPIs.
        # ----------------------------------------------------

        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        # ----------------------------------------------------
        # KPI 1 — Último ano
        # ----------------------------------------------------

        with col1:

            st.metric(
                "📅 Último ano",
                ultimo_ano_brasil_2
            )

        # ----------------------------------------------------
        # KPI 2 — Último valor
        # ----------------------------------------------------

        with col2:

            st.metric(
                "🇧🇷 Último valor",
                formatar_valor(
                    valor_brasil_2,
                    unidade_2
                )
            )

        # ----------------------------------------------------
        # KPI 3 — Menor valor
        # ----------------------------------------------------

        with col3:

            st.metric(
                "⬇️ Menor valor",
                formatar_valor(
                    minimo_brasil_2,
                    unidade_2
                )
            )

        # ----------------------------------------------------
        # KPI 4 — Maior valor
        # ----------------------------------------------------

        with col4:

            st.metric(
                "⬆️ Maior valor",
                formatar_valor(
                    maximo_brasil_2,
                    unidade_2
                )
            )

        # ----------------------------------------------------
        # KPI 5 — Variação até o maior
        # ----------------------------------------------------

        with col5:

            if variacao_maximo_brasil_2 is not None:

                st.metric(
                    "📈 Variação até o maior",
                    f"{variacao_maximo_brasil_2:.1f}%",
                    delta=f"{variacao_maximo_brasil_2:.1f}%",
                    delta_color="inverse"
                )

            else:

                st.metric(
                    "📈 Variação até o maior",
                    "—"
                )


# ============================================================
# 27. DIVISOR
# ============================================================

st.divider()


# ============================================================
# 28. COMPARAÇÃO ENTRE PAÍSES E REGIÕES
# ============================================================
#
# A comparação utiliza somente os países escolhidos pelo
# usuário.
#
# O ano utilizado é o último ano disponível dentro do
# intervalo selecionado.
#
# ============================================================

st.subheader(
    "🌎 Comparação entre países e regiões"
)

st.caption(
    f"Comparação dos países selecionados "
    f"no ano mais recente disponível: {ultimo_ano}."
)


# ============================================================
# 29. COMPARAÇÃO — UNIDADE 1
# ============================================================

st.markdown(
    f"### Comparação — {unidade_1_exibicao}"
)

dados_comparacao_1 = filtrado[
    (
        filtrado["Unidade"]
        == unidade_1
    )
    &
    (
        filtrado["Ano"]
        == ultimo_ano
    )
].copy()


if not dados_comparacao_1.empty:

    figura_comparacao_1 = (
        criar_grafico_comparativo(
            dados_comparacao_1,
            unidade_1,
            ultimo_ano,
        )
    )

    st.plotly_chart(
        figura_comparacao_1,
        width="stretch",
        config={
            "displaylogo": False,
        },
    )

else:

    st.info(
        f"Não existem dados para "
        f"{unidade_1_exibicao} "
        f"no ano {ultimo_ano}."
    )


# ============================================================
# 30. COMPARAÇÃO — UNIDADE 2
# ============================================================

st.markdown(
    f"### Comparação — {unidade_2_exibicao}"
)

dados_comparacao_2 = filtrado[
    (
        filtrado["Unidade"]
        == unidade_2
    )
    &
    (
        filtrado["Ano"]
        == ultimo_ano
    )
].copy()


if not dados_comparacao_2.empty:

    figura_comparacao_2 = (
        criar_grafico_comparativo(
            dados_comparacao_2,
            unidade_2,
            ultimo_ano,
        )
    )

    st.plotly_chart(
        figura_comparacao_2,
        width="stretch",
        config={
            "displaylogo": False,
        },
    )

else:

    st.info(
        f"Não existem dados para "
        f"{unidade_2_exibicao} "
        f"no ano {ultimo_ano}."
    )


# ============================================================
# 31. DIVISOR
# ============================================================

st.divider()


# ============================================================
# 32. EVOLUÇÃO AO LONGO DO TEMPO
# ============================================================
#
# Os gráficos são separados por unidade para evitar misturar
# escalas ou interpretações diferentes no mesmo gráfico.
#
# Cada linha representa um país/região.
#
# ============================================================

st.subheader(
    "📈 Evolução ao longo do tempo"
)

st.caption(
    "A evolução é apresentada separadamente "
    "para cada unidade."
)


# ============================================================
# 33. EVOLUÇÃO — UNIDADE 1
# ============================================================

st.markdown(
    f"### Evolução — {unidade_1_exibicao}"
)

dados_evolucao_1 = filtrado[
    filtrado[
        "Unidade"
    ] == unidade_1
].copy()


if not dados_evolucao_1.empty:

    figura_evolucao_1 = (
        criar_grafico_evolucao(
            dados_evolucao_1,
            unidade_1,
            (
                "Evolução do indicador — "
                f"{unidade_1_exibicao}"
            ),
        )
    )

    st.plotly_chart(
        figura_evolucao_1,
        width="stretch",
        config={
            "displaylogo": False,
        },
    )

else:

    st.info(
        f"Não existem dados para "
        f"{unidade_1_exibicao}."
    )


# ============================================================
# 34. EVOLUÇÃO — UNIDADE 2
# ============================================================

st.markdown(
    f"### Evolução — {unidade_2_exibicao}"
)

dados_evolucao_2 = filtrado[
    filtrado[
        "Unidade"
    ] == unidade_2
].copy()


if not dados_evolucao_2.empty:

    figura_evolucao_2 = (
        criar_grafico_evolucao(
            dados_evolucao_2,
            unidade_2,
            (
                "Evolução do indicador — "
                f"{unidade_2_exibicao}"
            ),
        )
    )

    st.plotly_chart(
        figura_evolucao_2,
        width="stretch",
        config={
            "displaylogo": False,
        },
    )

else:

    st.info(
        f"Não existem dados para "
        f"{unidade_2_exibicao}."
    )


# ============================================================
# 35. TABELA DE DADOS
# ============================================================
#
# Apresenta os registros efetivamente utilizados na análise.
#
# A coluna Unidade recebe o nome amigável somente nesta
# etapa de apresentação.
#
# ============================================================

st.divider()

st.subheader(
    "📋 Dados utilizados na análise"
)


# ------------------------------------------------------------
# Seleção das colunas relevantes.
# ------------------------------------------------------------

tabela = filtrado[
    [
        "Pais_Regiao",
        "Ano",
        "Unidade",
        "Valor",
        "Status_Dado",
    ]
].sort_values(
    [
        "Pais_Regiao",
        "Ano",
        "Unidade",
    ]
).copy()


# ------------------------------------------------------------
# Substitui o nome técnico pelo nome amigável.
# ------------------------------------------------------------

tabela["Unidade"] = tabela[
    "Unidade"
].map(
    nome_unidade_exibicao
)


# ============================================================
# 36. EXPANSOR DA TABELA
# ============================================================

with st.expander(
    "🔎 Ver dados da análise"
):

    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
        column_config={

            "Pais_Regiao": st.column_config.TextColumn(
                "País / região"
            ),

            "Ano": st.column_config.NumberColumn(
                "Ano",
                format="%d"
            ),

            "Unidade": st.column_config.TextColumn(
                "Unidade"
            ),

            "Valor": st.column_config.NumberColumn(
                "Valor",
                format="%.2f"
            ),

            "Status_Dado": st.column_config.TextColumn(
                "Status"
            ),
        },
    )


# ============================================================
# 37. EXPORTAÇÃO DOS DADOS
# ============================================================
#
# Converte a tabela filtrada para CSV e disponibiliza um
# botão para download.
#
# O arquivo contém somente os dados atualmente utilizados
# na análise.
#
# ============================================================

st.subheader(
    "⬇️ Exportação"
)


csv_download = tabela.to_csv(
    index=False
).encode(
    "utf-8"
)


st.download_button(
    label="Baixar dados filtrados",
    data=csv_download,
    file_name="dados_dieta_filtrados.csv",
    mime="text/csv",
    width="content",
)


# ============================================================
# 38. INFORMAÇÕES SOBRE A BASE
# ============================================================
#
# Esta seção apresenta informações gerais sobre o conjunto
# de dados original.
#
# IMPORTANTE:
# Os indicadores abaixo utilizam "df", ou seja, a base
# completa, e não somente os dados filtrados.
#
# ============================================================

st.divider()

st.subheader(
    "📚 Fonte e informações sobre os dados"
)


with st.expander(
    "Ver informações da base"
):

    # --------------------------------------------------------
    # Organização dos KPIs informativos.
    # --------------------------------------------------------

    info_col1, info_col2, info_col3, info_col4 = (
        st.columns(4)
    )

    # --------------------------------------------------------
    # Quantidade total de registros.
    # --------------------------------------------------------

    with info_col1:

        st.metric(
            "Registros",
            f"{len(df):,.0f}"
        )

    # --------------------------------------------------------
    # Quantidade de países/regiões distintos.
    # --------------------------------------------------------

    with info_col2:

        st.metric(
            "Países / regiões",
            f"{df['Pais_Regiao'].nunique():,.0f}"
        )

    # --------------------------------------------------------
    # Primeiro ano disponível.
    # --------------------------------------------------------

    with info_col3:

        st.metric(
            "Ano inicial",
            int(df["Ano"].min())
        )

    # --------------------------------------------------------
    # Último ano disponível.
    # --------------------------------------------------------

    with info_col4:

        st.metric(
            "Ano final",
            int(df["Ano"].max())
        )

    # --------------------------------------------------------
    # Informações adicionais.
    # --------------------------------------------------------

    st.write(
        f"**Publicação:** "
        f"{df['Publicacao'].iloc[0]}"
    )

    st.write(
        f"**Indicadores disponíveis:** "
        f"{df['Item_Analise'].nunique()}"
    )

    st.write(
        f"**Unidades disponíveis:** "
        f"{df['Unidade'].nunique()}"
    )


# ============================================================
# 39. RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🥗 Custo de uma Dieta Saudável | "
    "Aplicação desenvolvida em Python + Pandas + Plotly + Streamlit"
)


# ============================================================
# FIM DA APLICAÇÃO
# ============================================================
#
# FLUXO RESUMIDO
# ------------------------------------------------------------
#
#       CSV
#        │
#        ▼
#   carregar_dados()
#        │
#        ▼
#    DataFrame
#        │
#        ▼
#   Filtros Sidebar
#        │
#        ▼
#  Aplicar filtros
#        │
#        ▼
#   Dados filtrados
#        │
#        ├──────────────► KPIs Brazil
#        │
#        ├──────────────► Comparação entre países
#        │
#        ├──────────────► Evolução temporal
#        │
#        ├──────────────► Tabela
#        │
#        └──────────────► Download CSV
#
# ============================================================