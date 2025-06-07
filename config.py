"""
Configurações do Bot de Apostas no Telegram
------------------------------------------
Este arquivo contém as configurações do bot.
As variáveis de ambiente são usadas para configurações sensíveis.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (para desenvolvimento local)
load_dotenv()

# Token do Bot do Telegram (obtido do BotFather)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7538547502:AAElp6bSncYy6K2ZBSHR-DSrlptq7jcF3i4")

# Chave da API de odds (TheOddsAPI - https://theoddsapi.com/)
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")

# Nome de usuário do bot
BOT_USERNAME = os.getenv("BOT_USERNAME", "Cadastroinfratores_bot")

# ID do usuário administrador (opcional)
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", None)
if ADMIN_USER_ID and ADMIN_USER_ID.isdigit():
    ADMIN_USER_ID = int(ADMIN_USER_ID)
else:
    ADMIN_USER_ID = None

# URL da aplicação (para configuração de webhook)
APP_URL = os.getenv("APP_URL", "")

# Porta para o servidor web
PORT = int(os.getenv("PORT", "8080"))

# Configurações de apostas
DEFAULT_SPORT = os.getenv("DEFAULT_SPORT", "soccer")  # Esporte padrão para buscar jogos
ODDS_REGIONS = os.getenv("ODDS_REGIONS", "eu")  # Região para formato de odds (eu, uk, us)
MIN_VALUE_THRESHOLD = float(os.getenv("MIN_VALUE_THRESHOLD", "1.5"))  # Valor mínimo de odd para considerar uma aposta

# Configurações de notificações
DAILY_NOTIFICATION_TIME = os.getenv("DAILY_NOTIFICATION_TIME", "09:00")  # Horário para envio automático de sugestões (formato 24h)

# Configuração para usar dados simulados (True) ou dados reais (False)
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "True").lower() == "true"

# Configuração de debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

