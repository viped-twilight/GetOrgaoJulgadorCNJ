import streamlit as st
from datajud import DataJud, get_endpoint
from typing import Literal
import json

st.title("Consulta de Órgão Julgador - CNJ")
st.markdown("### Justiça Federal e Justiça Estadual")

# Criação das abas
tab_search, tab_about = st.tabs(["Consultar", "Sobre"])

with tab_search:
    st.header("Consultar Processo")

    # Input para número processual unificado
    numero_processo:str|None = st.text_input("Digite o número processual unificado:")
    numero_processo = numero_processo.replace('-', "").replace('.', "")

    # Instanciando DataJud ao iniciar
    datajud:DataJud = DataJud()

    # Botão para consultar
    if st.button("Consultar órgão julgador"):
        if numero_processo:
            try:
                info_proc = datajud.requestDATAJUD(
                    url=get_endpoint(numero_processo),
                    api_key=datajud.API_KEY,
                    num_processo=numero_processo
                    )

                history = info_proc.get("hits", {}).get("hits", [])
                if not history:
                    st.error("Nenhum resultado encontrado para o processo informado.")
                else:
                    info_orgao = {}
                    for i, item in enumerate(history):
                        info_orgao.__setitem__(
                            i, item["_source"]["orgaoJulgador"]
                        )
            
                    st.subheader("Informações do órgão julgador:")
                    st.json(info_orgao)
            except Exception as e:
                st.error(f"Ocorreu um erro ao consultar o processo: {e}")
        else:
            st.warning("Por favor, digite o número do processo.")

with tab_about:
    st.header("Sobre a Aplicação")
    st.markdown("""
    ### Finalidade
    Esta aplicação foi desenvolvida para facilitar a consulta do **órgão julgador** de um processo judicial diretamente da base de dados do DataJud, mantida pelo Conselho Nacional de Justiça (CNJ).

    ### Como Utilizar
    1.  Navegue até a aba **"Consultar"**;
    2.  Insira o número do processo no formato unificado (ex: `0000000-00.0000.0.00.0000`);
    3.  Clique no botão **"Consultar órgão julgador"**;
    4.  O histórico de órgãos por onde o processo tramitou será exibido em formato JSON.

    ### Limitações
    - A consulta é restrita a processos da **Justiça Federal** e **Justiça Estadual**;
    - A precisão e a disponibilidade das informações dependem exclusivamente da API do DataJud.
    """)
    
    st.header("Tribunais Suportados")
    try:
        # Carregar dados dos tribunais
        with open("data/justicafederal.json", "r") as f:
            justica_federal = json.load(f)
        
        with open("data/justicaestadual.json", "r") as f:
            justica_estadual = json.load(f)

        # Preparar dados para a tabela
        tribunais = {
            "Tribunal": [vf.upper() for vf in justica_federal.values()] + [ve.upper() for ve in justica_estadual.values()],
            "Tipo": ["Federal"] * len(justica_federal) + ["Estadual"] * len(justica_estadual)
        }
        
        st.table(tribunais)

    except FileNotFoundError:
        st.error("Arquivos de dados dos tribunais não encontrados na pasta 'data'.")
    except json.JSONDecodeError:
        st.error("Erro ao ler os arquivos JSON dos tribunais.")