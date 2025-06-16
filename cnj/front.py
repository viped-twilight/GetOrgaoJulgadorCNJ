import streamlit as st
from datajud import DataJud
import json

st.title("Consulta de Órgão Julgador - CNJ (Justiça Federal)")

# Input para número processual unificado
numero_processo = st.text_input("Digite o número processual unificado:")
numero_processo = numero_processo.replace('-', "").replace('.', "")

# NNNNNNN-DD.AAAA.J.TR.OOOO
# 0123456 78 9ABC D EF
trf_cod = numero_processo[14:16]

with open("../data/justicafederal.json", "r") as f:
    trf = json.load(f)[trf_cod]

endpoint =  f"https://api-publica.datajud.cnj.jus.br/api_publica_{trf}/_search"
# Instanciando DataJud ao iniciar
datajud = DataJud(url=endpoint)

# Botão para consultar
if st.button("Consultar órgão julgador"):
    if numero_processo:
        info_orgao = datajud.requestDATAJUD(numero_processo)
        st.subheader("Informações do órgão julgador:")
        st.json(info_orgao)
    else:
        st.warning("Por favor, digite o número do processo.")