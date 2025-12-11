from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import urllib3
import os

# Desabilita avisos chatos sobre certificado SSL (apenas para dev local)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(
    title="API de conversão de moedas",
    description="Microserviço de conversão de moedas containerizado.",
    version="1.0.0"
)

# --- ROTA 1: Health Check (Para saber se o sistema está vivo) ---
@app.get("/")
# def read_root():
#     return {
#         "status": "online", 
#         "service": "Currency Converter", 
#         "tech": "FastAPI + Docker"
#     }

# --- ROTA 1: A NOVA PÁGINA BONITA ---
@app.get("/")
def read_root():
    # Retorna o arquivo HTML em vez do JSON
    return FileResponse("index.html")

# --- ROTA 2: Conversão Principal ---
@app.get("/convert/{from_currency}/{to_currency}/{amount}")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    """
    Converte um valor entre duas moedas usando taxas em tempo real.
    Ex: /convert/USD/BRL/100
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    # Tenta usar a AwesomeAPI (Melhor para pares com BRL)
    url = f"https://json.awesomeapi.com.br/last/{from_currency}-{to_currency}"
    
    try:
        # TRUQUE: Cabeçalhos para fingir ser um navegador Google Chrome
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # verify=False ajuda a rodar no Windows sem erro de certificado
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        # Se a API principal falhar, tenta o fallback
        if response.status_code != 200:
            print(f"⚠️ AwesomeAPI falhou ({response.status_code}), tentando fallback...")
            return calculate_international(from_currency, to_currency, amount)
        
        data = response.json()
        key = f"{from_currency}{to_currency}"
        
        # Se a chave não existir (ex: par raro), tenta fallback
        if key not in data:
            return calculate_international(from_currency, to_currency, amount)

        bid_price = float(data[key]['bid'])
        converted_value = round(amount * bid_price, 2)
        
        return {
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "rate": bid_price,
            "converted_value": converted_value,
            "source": "AwesomeAPI (Real-time)"
        }
        
    except Exception as e:
        print(f"🔴 Erro na API principal: {e}")
        # Se der erro de conexão, tenta a secundária
        return calculate_international(from_currency, to_currency, amount)

# --- FUNÇÃO AUXILIAR: Fallback (Plano B) ---
def calculate_international(base, target, amount):
    """
    Usa uma API internacional (Open Exchange Rates) caso a brasileira falhe.
    """
    try:
        # API alternativa gratuita que não exige chave
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, verify=False, timeout=10)
        data = response.json()
        
        if target not in data['rates']:
            raise HTTPException(status_code=404, detail=f"Moeda {target} não suportada.")
            
        rate = data['rates'][target]
        return {
            "from": base,
            "to": target,
            "amount": amount,
            "rate": rate,
            "converted_value": round(amount * rate, 2),
            "source": "Open ER API (Fallback)"
        }
    except Exception as e:
        print(f"🔴 Erro fatal no fallback: {e}")
        raise HTTPException(status_code=503, detail="Serviço de câmbio indisponível no momento.")