import streamlit as st
from datajud import DataJud
import json

st.title("Consulta de Órgão Julgador - CNJ (Justiça Federal)")

# Input para número processual unificado
numero_processo = st.text_input("Digite o número processual unificado:")
numero_processo = numero_processo.replace('-', "").replace('.', "")

# Instanciando DataJud ao iniciar
datajud = DataJud()

# Botão para consultar
if st.button("Consultar órgão julgador"):
    if numero_processo:
        info_proc = datajud.requestDATAJUD(
            url=get_endpoint(numero_processo),
            api_key=datajud.api_key,
            num_processo=numero_processo)
        
        info_orgao = info_proc
        st.subheader("Informações do órgão julgador:")
        st.json(info_orgao)
    else:
        st.warning("Por favor, digite o número do processo.")