import pandas as pd
import requests
from typing import Dict

class DataJud:
    """
    A class designed to interact with the DATAJUD API and process statistical data related to judicial processes.

    ...
    
    Attributes
    ----------
    url str
        The URL endpoint for the DATAJUD API (default: "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search").
    API_KEY : str
        The public API key for accessing the DATAJUD API.
    tab_estatistica : pd.DataFrame, optional
        A pandas DataFrame containing statistical data from DATAJUD.

    Methods
    -------
    **requestDATAJUD**(**url**: _str_, **api_key**: _str_, **num_processo**: _str_) -> _dict_ <br />
        Sends a request to the DATAJUD API for a specific judicial process and returns the response as a dictionary.
    **get_processo_from_painel_estatistico_of_DATAJUD**(**tab_estatistica**: _pd.DataFrame_, **num_processo**: _str_) -> _pd.DataFrame_ <br />
        Searches for a specific judicial process in the statistical data table and returns the matching rows as a DataFrame.
    """
    def __init__(
            self:"DataJud", 
            url:str = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search", # URL de Solicitação ao TRF1
            api_key:str = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",  # API pública do DATAJUD 
            tab_estatistica: pd.DataFrame = ...
        ) -> None:
        
        self.url = url
        self.API_KEY = api_key
        if tab_estatistica is not None:
            self.tab_estatistica = tab_estatistica

        return None

    def requestDATAJUD(
            self: "DataJud",
            url:str,
            api_key:str,
            num_processo:str
        ) -> dict:
        """
        Realiza a requisição de um processo à API do DATAJUD e
        retorna como resultado um dicionário com todas as informações
        fornecidas na resposta.

        Parameters
        ----------
        url (str)
            Url da API.
        api_key (str) 
            Chave pública da API DATAJUD.
        num_processo (str)
            Número do processo pesquisado.
        
        Returns
        -------
        dict_response (dict)
            Dicionário com as informações do processo.
        """

        num_processo = num_processo.replace('-', "").replace('.', "")

        payload = json.dumps({
        "query": {
            "match": {
            "numeroProcesso": num_processo
            }
        }
        })

        headers = {
        'Authorization': f'ApiKey {api_key}',
        'Content-Type': 'application/json'
        }

        for i in range(50):
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                break
            else:
                print(f"Request failed with status {response.status_code}. Retrying...")

        dict_response = dict(response.json())
        return dict_response
    
    def get_processo_from_painel_estatistico_of_DATAJUD(
            self:"DataJud",
            tab_estatistica:pd.DataFrame, 
            num_processo:str
        ) -> "pd.DataFrame":
        """
        Parameters
        ----------
        tab_estatistica (pd.DataFrame) : Tabela .csv de dados estatísticos do DATAJUD.
        num_processo (str) : Número do processo pesquisado.
        
        Returns
        -------
            query (pd.DataFrame) : Resultado da pesquisa pelo processo fornecido.
        """
        if self.tab_estatistica is not None:
            df = self.tab_estatistica
        else:
            df = tab_estatistica
        infos = df.columns.str.lower()
        infos = infos.str.replace(" ", "_")

        query = df.query("Processo == @num_processo")
        query.columns = infos

        return query

def get_endpoint(num_processo:str) -> str:
    # NNNNNNN-DD.AAAA.J.TR.OOOO
    # 0123456 78 9ABC D EF
    trf_cod = num_processo[14:16]
    
    with open("data/justicafederal.json", "r") as f:
        trf = json.load(f)[trf_cod]
    
    endpoint =  f"https://api-publica.datajud.cnj.jus.br/api_publica_{trf}/_search"

    return endpoint