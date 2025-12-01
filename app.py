import streamlit as st
from datetime import datetime, timedelta

# --- Funções de Conversão ---

def gregorian_to_julian(gregorian_date_str):
    """
    Converte uma data Gregoriana (DD/MM/AAAA) para o formato Juliano (CYYDDD).
    C = Dígito do século (ex: 1 para 2000-2099)
    YY = Últimos dois dígitos do ano
    DDD = Dia do ano (001 a 366)
    Exemplo: 01/01/2025 -> 125001
    """
    try:
        # Assumindo o formato DD/MM/AAAA (padrão brasileiro)
        date_obj = datetime.strptime(gregorian_date_str, '%d/%m/%Y')
        
        year = date_obj.year
        
        # Dígito do século (C)
        # 2000-2099 -> 1
        # 2100-2199 -> 2
        century_digit = str(year // 100 - 19) # 2025 // 100 = 20. 20 - 19 = 1.
        
        # Últimos dois dígitos do ano (YY)
        year_yy = date_obj.strftime('%y')
        
        # Dia do ano (DDD)
        day_of_year = date_obj.strftime('%j')
        
        # Formato Juliano CYYDDD
        julian_date = f"{century_digit}{year_yy}{day_of_year}"
        
        return julian_date
    except ValueError:
        return "Erro: Formato de data Gregoriana inválido. Use DD/MM/AAAA."

def julian_to_gregorian(julian_date_str):
    """
    Converte uma data Juliano (CYYDDD) para o formato Gregoriano (DD/MM/AAAA).
    C = Dígito do século (ex: 1 para 2000-2099)
    YY = Últimos dois dígitos do ano
    DDD = Dia do ano (001 a 366)
    Exemplo: 125001 -> 01/01/2025
    """
    if len(julian_date_str) != 6 or not julian_date_str.isdigit():
        return "Erro: Formato de data Juliano inválido. Use CYYDDD (6 dígitos)."
    
    try:
        # Extrai o dígito do século (C), ano (YY) e dia do ano (DDD)
        century_digit = int(julian_date_str[0])
        year_yy = int(julian_date_str[1:3])
        day_of_year = julian_date_str[3:]
        day_of_year_int = int(day_of_year)
        
        if not (1 <= day_of_year_int <= 366):
            return "Erro: Dia do ano fora do intervalo válido (001-366)."

        # Converte para o ano de quatro dígitos (AAAA)
        # Ex: C=1, YY=25 -> (1 + 19) * 100 + 25 = 2025
        full_year = (century_digit + 19) * 100 + year_yy
        
        # Cria a data: 1º de janeiro do ano + (dia do ano - 1) dias
        start_of_year = datetime(full_year, 1, 1)
        date_obj = start_of_year + timedelta(days=day_of_year_int - 1)
        
        # Verifica se o dia do ano é válido para o ano (ex: 366 em ano não bissexto)
        if date_obj.year != full_year:
             return "Erro: Dia do ano inválido para o ano especificado (possível ano não bissexto)."

        # Formato Gregoriano DD/MM/AAAA
        gregorian_date = date_obj.strftime('%d/%m/%Y')
        
        return gregorian_date
    except ValueError as e:
        return f"Erro de conversão: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"

# --- Interface Streamlit ---

st.set_page_config(
    page_title="Conversor de Data Juliano/Gregoriano",
    layout="centered"
)

st.title("🗓️ Conversor de Data Juliano ↔️ Gregoriano")
st.markdown("""
Este aplicativo converte datas entre o formato **Gregoriano (DD/MM/AAAA)** e o formato **Juliano (CYYDDD)**.
O formato Juliano é composto por:
*   **C**: Dígito do século (ex: **1** para 2000-2099)
*   **YY**: Últimos dois dígitos do ano (ex: **25** para 2025)
*   **DDD**: Dia do ano (001 a 366)

**Exemplo:** `01/01/2025` é `125001`.
""")

tab1, tab2 = st.tabs(["Gregoriano para Juliano", "Juliano para Gregoriano"])

with tab1:
    st.header("Gregoriano (DD/MM/AAAA) para Juliano (CYYDDD)")
    gregorian_input = st.text_input(
        "Insira a data Gregoriana (Ex: 01/01/2025)",
        placeholder="DD/MM/AAAA",
        key="greg_input"
    )
    
    if st.button("Converter para Juliano", key="btn_greg"):
        if gregorian_input:
            result = gregorian_to_julian(gregorian_input.strip())
            if result.startswith("Erro"):
                st.error(result)
            else:
                st.success(f"**Data Juliano:** `{result}`")
        else:
            st.warning("Por favor, insira uma data Gregoriana.")

with tab2:
    st.header("Juliano (CYYDDD) para Gregoriano (DD/MM/AAAA)")
    julian_input = st.text_input(
        "Insira a data Juliano (Ex: 125001)",
        placeholder="CYYDDD",
        key="julian_input"
    )
    
    if st.button("Converter para Gregoriano", key="btn_julian"):
        if julian_input:
            result = julian_to_gregorian(julian_input.strip())
            if result.startswith("Erro"):
                st.error(result)
            else:
                st.success(f"**Data Gregoriana:** `{result}`")
        else:
            st.warning("Por favor, insira uma data Juliano.")

st.markdown("---")
st.caption("Desenvolvido com Python e Streamlit.")