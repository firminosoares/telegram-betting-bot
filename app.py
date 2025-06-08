"""
Bot de Apostas no Telegram - Aplicação Principal
----------------------------------------------
Este é o arquivo principal que implementa o bot do Telegram
usando Flask e webhooks para funcionar no Railway.app.
"""

import os
import logging
from datetime import datetime, time
import asyncio
import json
from flask import Flask, request, jsonify
import pytz

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler
)

from config import (
    TELEGRAM_TOKEN, BOT_USERNAME, ADMIN_USER_ID,
    DEFAULT_SPORT, DAILY_NOTIFICATION_TIME,
    APP_URL, PORT, DEBUG
)
from data_collector import DataCollector
from analyzer import BettingAnalyzer

# Configurar logging
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)

# Variáveis globais para cache de dados
games_data = None
odds_data = None
last_update = None
telegram_app = None

# Instância do coletor de dados
data_collector = DataCollector()

async def update_data():
    """Atualiza os dados de jogos e odds."""
    global games_data, odds_data, last_update
    
    logger.info("Atualizando dados...")
    
    try:
        # Obter dados
        games, odds = data_collector.get_todays_games_and_odds(DEFAULT_SPORT)
        
        if games and odds:
            games_data = data_collector.format_games_data(games)
            odds_data = data_collector.format_odds_data(odds)
            last_update = datetime.now()
            logger.info(f"Dados atualizados com sucesso. {len(games)} jogos e {len(odds)} jogos com odds.")
            return True
        else:
            logger.warning("Não foi possível atualizar os dados: dados vazios.")
            return False
    except Exception as e:
        logger.error(f"Erro ao atualizar dados: {e}")
        return False

# Comandos do bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia mensagem quando o comando /start é emitido."""
    user = update.effective_user
    await update.message.reply_text(
        f"Olá, {user.first_name}! 👋\n\n"
        f"Bem-vindo ao Bot de Apostas! Estou aqui para te ajudar com sugestões de apostas.\n\n"
        f"Use /apostas para ver as sugestões de hoje.\n"
        f"Use /ajuda para ver todos os comandos disponíveis."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia mensagem de ajuda quando o comando /ajuda é emitido."""
    help_text = (
        "🤖 *Comandos disponíveis:*\n\n"
        "/start - Inicia o bot\n"
        "/apostas - Mostra sugestões de apostas para hoje\n"
        "/jogos - Lista os jogos do dia\n"
        "/odds - Mostra as odds para um jogo específico\n"
        "/status - Mostra o status atual do bot\n"
        "/refresh - Atualiza manualmente os dados\n"
        "/ajuda - Mostra esta mensagem de ajuda\n\n"
        "Enviarei automaticamente sugestões de apostas todos os dias pela manhã! ⚽🏀🎾"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def bets_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia sugestões de apostas quando o comando /apostas é emitido."""
    await update.message.reply_text("Buscando sugestões de apostas para hoje... ⏳")
    
    # Verificar se há dados disponíveis
    if games_data is None or odds_data is None:
        success = await update_data()
        if not success:
            await update.message.reply_text(
                "❌ Não foi possível obter dados para gerar sugestões.\n"
                "Por favor, tente novamente mais tarde."
            )
            return
    
    # Gerar sugestões
    try:
        analyzer = BettingAnalyzer(games_data, odds_data)
        suggestions = analyzer.generate_suggestions(max_suggestions=5)
        
        if not suggestions:
            await update.message.reply_text(
                "Não foram encontradas sugestões de apostas para hoje.\n"
                "Tente novamente mais tarde ou use /jogos para ver os jogos disponíveis."
            )
            return
        
        message = analyzer.format_suggestions_message(suggestions)
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao gerar sugestões: {e}")
        await update.message.reply_text(
            "❌ Ocorreu um erro ao gerar sugestões.\n"
            "Por favor, tente novamente mais tarde."
        )

async def games_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista os jogos do dia quando o comando /jogos é emitido."""
    await update.message.reply_text("Buscando jogos para hoje... ⏳")
    
    # Verificar se há dados disponíveis
    if games_data is None:
        success = await update_data()
        if not success:
            await update.message.reply_text(
                "❌ Não foi possível obter dados de jogos.\n"
                "Por favor, tente novamente mais tarde."
            )
            return
    
    # Formatar mensagem com jogos
    try:
        if games_data.empty:
            await update.message.reply_text("Não foram encontrados jogos para hoje.")
            return
        
        today = datetime.now().strftime("%d/%m/%Y")
        message = f"🗓️ *Jogos de Hoje - {today}*\n\n"
        
        # Agrupar jogos por liga
        leagues = games_data['league'].unique()
        
        for league in leagues:
            league_games = games_data[games_data['league'] == league]
            message += f"⚽ *{league}*\n"
            
            for _, game in league_games.iterrows():
                home = game['home_team']
                away = game['away_team']
                time = game['time'] if 'time' in game else "Horário não disponível"
                
                message += f"• {home} x {away} - {time}\n"
            
            message += "\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao listar jogos: {e}")
        await update.message.reply_text(
            "❌ Ocorreu um erro ao listar os jogos.\n"
            "Por favor, tente novamente mais tarde."
        )

async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra as odds para um jogo específico quando o comando /odds é emitido."""
    # Verificar se há dados disponíveis
    if odds_data is None:
        success = await update_data()
        if not success:
            await update.message.reply_text(
                "❌ Não foi possível obter dados de odds.\n"
                "Por favor, tente novamente mais tarde."
            )
            return
    
    if not odds_data:
        await update.message.reply_text(
            "❌ Não há dados de odds disponíveis no momento.\n"
            "Por favor, tente novamente mais tarde."
        )
        return
    
    # Criar teclado inline com jogos disponíveis
    keyboard = []
    for game in list(odds_data.keys())[:10]:  # Limitar a 10 jogos
        keyboard.append([InlineKeyboardButton(game, callback_data=f"odds_{game}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Selecione um jogo para ver as odds:",
        reply_markup=reply_markup
    )

async def show_odds(update: Update, game: str) -> None:
    """Mostra as odds para um jogo específico."""
    try:
        game_data = odds_data[game]
        
        # Formatar mensagem com odds
        message = f"📊 *Odds para {game}*\n\n"
        
        for bookie_name, markets in game_data.get('bookmakers', {}).items():
            message += f"*{bookie_name.upper()}*\n"
            
            # Resultado Final (h2h)
            if 'h2h' in markets:
                message += "🏆 *Resultado Final*\n"
                for outcome, price in markets['h2h'].items():
                    outcome_name = "Empate" if outcome == "Draw" else f"Vitória {outcome}"
                    message += f"• {outcome_name}: {price:.2f}\n"
                message += "\n"
            
            # Total de Gols (totals)
            if 'totals' in markets:
                message += "🎯 *Total de Gols*\n"
                for outcome, price in markets['totals'].items():
                    outcome_name = f"Over {outcome[1:]}" if outcome.startswith('O') else f"Under {outcome[1:]}"
                    message += f"• {outcome_name}: {price:.2f}\n"
                message += "\n"
        
        # Verificar se a mensagem é uma resposta a um callback
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao mostrar odds: {e}")
        
        # Verificar se a mensagem é uma resposta a um callback
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(
                "❌ Ocorreu um erro ao mostrar as odds.\n"
                "Por favor, tente novamente mais tarde."
            )
        else:
            await update.message.reply_text(
                "❌ Ocorreu um erro ao mostrar as odds.\n"
                "Por favor, tente novamente mais tarde."
            )

async def refresh_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Atualiza manualmente o cache de dados."""
    await update.message.reply_text("Atualizando dados de jogos e odds... ⏳")
    
    success = await update_data()
    
    if success:
        await update.message.reply_text(
            "✅ Dados atualizados com sucesso!\n\n"
            f"Jogos encontrados: {len(games_data) if games_data is not None else 0}\n"
            f"Jogos com odds: {len(odds_data) if odds_data is not None else 0}\n"
            f"Última atualização: {last_update.strftime('%d/%m/%Y %H:%M:%S') if last_update else 'N/A'}"
        )
    else:
        await update.message.reply_text(
            "❌ Não foi possível atualizar os dados.\n"
            "Por favor, tente novamente mais tarde."
        )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra o status atual do bot e do cache de dados."""
    status_message = (
        "📊 *Status do Bot de Apostas*\n\n"
        f"🤖 Bot: @{BOT_USERNAME}\n"
        f"🕒 Horário atual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"🔄 Última atualização de dados: {last_update.strftime('%d/%m/%Y %H:%M:%S') if last_update else 'Nunca'}\n\n"
        f"📈 Jogos em cache: {len(games_data) if games_data is not None else 0}\n"
        f"📊 Jogos com odds: {len(odds_data) if odds_data is not None else 0}\n"
        f"⏰ Horário de notificações diárias: {DAILY_NOTIFICATION_TIME}\n\n"
        f"Use /refresh para atualizar os dados manualmente."
    )
    
    await update.message.reply_text(status_message, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processa callbacks de botões inline."""
    query = update.callback_query
    data = query.data
    
    # Processar diferentes tipos de callbacks
    if data.startswith("odds_"):
        game = data[5:]  # Remover prefixo "odds_"
        await show_odds(update, game)
    else:
        await query.answer("Comando não reconhecido")

def setup_telegram_app():
    """Configura a aplicação do Telegram."""
    global telegram_app
    
    # Criar o aplicativo e passar o token do bot
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Adicionar handlers de comando
    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(CommandHandler("ajuda", help_command))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(CommandHandler("apostas", bets_command))
    telegram_app.add_handler(CommandHandler("jogos", games_command))
    telegram_app.add_handler(CommandHandler("odds", odds_command))
    telegram_app.add_handler(CommandHandler("refresh", refresh_command))
    telegram_app.add_handler(CommandHandler("status", status_command))
    
    # Adicionar handler para botões inline
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info(f"Bot @{BOT_USERNAME} configurado!")

# Rotas Flask
@app.route('/')
def index():
"""Rota principal para verificar se o serviço está funcionando."""
    return f"""
    <html>
    <head>
        <title>Bot de Apostas - Status</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .status {{ background: #e8f5e8; padding: 20px; border-radius: 8px; }}
            .button {{ background: #007bff; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px; margin: 10px; 
                      display: inline-block; }}
            .button:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <h1>🤖 Bot de Apostas no Telegram</h1>
        
        <div class="status">
            <h2>✅ Status: Online</h2>
            <p><strong>Bot:</strong> @{BOT_USERNAME}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Jogos em cache:</strong> {len(games_data) if games_data is not None else 0}</p>
            <p><strong>Odds em cache:</strong> {len(odds_data) if odds_data is not None else 0}</p>
        </div>
        
        <h3>🔧 Configuração do Webhook:</h3>
        <a href="/clear_webhook" class="button">🗑️ Limpar Webhook Atual</a>
        <a href="/set_webhook" class="button">⚙️ Configurar Novo Webhook</a>
        
        <h3>📊 Endpoints Disponíveis:</h3>
        <ul>
            <li><a href="/">/</a> - Esta página</li>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/webhook">/webhook</a> - Endpoint do webhook (POST)</li>
            <li><a href="/set_webhook">/set_webhook</a> - Configurar webhook</li>
            <li><a href="/clear_webhook">/clear_webhook</a> - Limpar webhook</li>
        </ul>
        
        <p><em>Para testar o bot, envie /start para @{BOT_USERNAME} no Telegram</em></p>
    </body>
    </html>
    """
```

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint para receber updates do Telegram via webhook."""
    try:
        # Obter dados do request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({"error": "No JSON data"}), 400
        
        # Criar objeto Update
        update = Update.de_json(json_data, telegram_app.bot)
        
        # Processar update de forma assíncrona
        asyncio.create_task(telegram_app.process_update(update))
        
        return jsonify({"status": "ok"})
    
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/set_webhook', methods=['GET','POST'])
def set_webhook():
    """Configura o webhook do Telegram."""
    try:
        if not APP_URL:
            # Tentar obter URL automaticamente
            app_url = request.host_url.rstrip('/')
        else:
            app_url = APP_URL.rstrip('/')
        
        webhook_url = f"{app_url}/webhook"
        
        # Primeiro, limpar webhook existente
        clear_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
        clear_response = requests.post(clear_url)
        
        # Configurar novo webhook
        set_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        data = {"url": webhook_url}
        
        response = requests.post(set_url, json=data)
        result = response.json()
        
        if result.get("ok"):
            return f"""
            <html>
            <body>
                <h2>✅ Webhook Configurado com Sucesso!</h2>
                <p><strong>URL do Webhook:</strong> {webhook_url}</p>
                <p><strong>Status:</strong> {result.get('description', 'OK')}</p>
                <p>Agora teste o bot no Telegram enviando /start</p>
                <a href="/">← Voltar para página inicial</a>
            </body>
            </html>
            """
        else:
            return f"""
            <html>
            <body>
                <h2>❌ Erro ao Configurar Webhook</h2>
                <p><strong>Erro:</strong> {result.get('description', 'Erro desconhecido')}</p>
                <a href="/">← Voltar para página inicial</a>
            </body>
            </html>
            """
    
    except Exception as e:
        return f"""
        <html>
        <body>
            <h2>❌ Erro Interno</h2>
            <p><strong>Erro:</strong> {str(e)}</p>
            <a href="/">← Voltar para página inicial</a>
        </body>
        </html>
               """
```

@app.route('/clear_webhook', methods=['GET', 'POST'])
def clear_webhook():
    """Remove o webhook atual do Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
        response = requests.post(url)
        result = response.json()
        
        if result.get("ok"):
            return f"""
            <html>
            <body>
                <h2>✅ Webhook Removido com Sucesso!</h2>
                <p>O webhook anterior foi removido.</p>
                <p><a href="/set_webhook">Configurar novo webhook</a></p>
                <a href="/">← Voltar para página inicial</a>
            </body>
            </html>
            """
        else:
            return f"""
            <html>
            <body>
                <h2>❌ Erro ao Remover Webhook</h2>
                <p><strong>Erro:</strong> {result.get('description', 'Erro desconhecido')}</p>
                <a href="/">← Voltar para página inicial</a>
            </body>
            </html>
            """
    
    except Exception as e:
        return f"""
        <html>
        <body>
            <h2>❌ Erro Interno</h2>
            <p><strong>Erro:</strong> {str(e)}</p>
            <a href="/">← Voltar para página inicial</a>
        </body>
        </html>
        """
```

@app.route('/health')
def health():
    """Endpoint de health check."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Configurar aplicação do Telegram
    setup_telegram_app()
    
    # Atualizar dados iniciais
    asyncio.run(update_data())
    
    # Iniciar servidor Flask
    logger.info(f"Iniciando servidor na porta {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

