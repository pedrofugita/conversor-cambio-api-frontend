# 💱 Currency Exchange Microservice

## 📌 Sobre o Projeto
Este é um microserviço de conversão monetária de alta performance, desenvolvido com **FastAPI** e arquitetura **Cloud-Native**.

O diferencial deste projeto é a sua **Resiliência**:
1. O sistema consome uma API brasileira (AwesomeAPI) para dados em tempo real de cotação de moedas.
2. Caso a API principal falhe ou não tenha a moeda, o sistema ativa automaticamente um **Fallback** para uma API internacional (Open Exchange Rates), garantindo que o serviço nunca pare (High Availability).
3. Possui um Frontend moderno para consumo fácil pelo usuário final.

## 🚀 Funcionalidades
- **Full Stack:** Backend em Python (FastAPI) e Frontend em HTML5/CSS/JS.
- **Multi-Moeda:** Suporte para BRL, USD, EUR, BTC, JPY, entre outras.
- **Failover Strategy:** Tratamento de erros robusto com troca automática de provedor de dados.
- **Auto-Documentation:** Documentação técnica automática via Swagger UI.
- **Dockerized:** Pronto para deploy em containers.

## 🛠 Tech Stack
- **Linguagem:** Python 3.10+
- **Framework:** FastAPI (ASGI)
- **Frontend:** HTML5, CSS3 (Responsivo)
- **Container:** Docker

## 🐳 Como Rodar

### Opção A: Via Docker (Recomendado)
```bash
    # 1. Construir a imagem
    docker build -t currency-api .

    # 2. Rodar o container
    docker run -p 8000:8000 currency-api
```

### Opção B: Localmente (Python)
```bash
    # 1. Instalar dependências
    pip install -r requirements.txt

    # 2. Rodar o servidor
    uvicorn main:app --reload
```

## 🧪 Acessando o Projeto
- **Interface Web:** Acesse http://localhost:8000/ para usar o conversor.
- **Documentação Técnica (Swagger):** Acesse http://localhost:8000/docs para testar os endpoints da API.

---

Desenvolvido como case técnico de Engenharia de Software por Pedro Fugita.