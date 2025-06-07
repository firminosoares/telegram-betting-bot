"""
Módulo de Coleta de Dados
------------------------
Este módulo é responsável por coletar dados de jogos e odds
de APIs externas ou usar dados simulados.
"""

import requests
import logging
from datetime import datetime
import pandas as pd
from config import ODDS_API_KEY, USE_MOCK_DATA
from mock_data import MOCK_GAMES, MOCK_ODDS

logger = logging.getLogger(__name__)

class DataCollector:
    """Classe para coleta de dados de jogos e odds."""
    
    def __init__(self):
        """Inicializa o coletor de dados."""
        self.api_key = ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4"
        
    def get_sports(self):
        """
        Obtém lista de esportes disponíveis.
        
        Returns:
            list: Lista de esportes disponíveis
        """
        if USE_MOCK_DATA:
            return [
                {"key": "soccer_epl", "title": "Premier League"},
                {"key": "soccer_laliga", "title": "La Liga"},
                {"key": "soccer_serie_a", "title": "Serie A"},
                {"key": "soccer_bundesliga", "title": "Bundesliga"}
            ]
        
        try:
            url = f"{self.base_url}/sports"
            params = {"apiKey": self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao obter esportes: {e}")
            return []
    
    def get_games(self, sport="soccer"):
        """
        Obtém jogos para um esporte específico.
        
        Args:
            sport (str): Chave do esporte
            
        Returns:
            list: Lista de jogos
        """
        if USE_MOCK_DATA:
            logger.info("Usando dados simulados para jogos")
            return MOCK_GAMES
        
        try:
            url = f"{self.base_url}/sports/{sport}/events"
            params = {
                "apiKey": self.api_key,
                "dateFormat": "iso"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            games = response.json()
            logger.info(f"Obtidos {len(games)} jogos para {sport}")
            return games
        except Exception as e:
            logger.error(f"Erro ao obter jogos para {sport}: {e}")
            return []
    
    def get_odds(self, sport="soccer", markets="h2h,totals", regions="eu"):
        """
        Obtém odds para um esporte específico.
        
        Args:
            sport (str): Chave do esporte
            markets (str): Mercados de apostas (h2h, totals, spreads)
            regions (str): Regiões das odds (eu, uk, us)
            
        Returns:
            list: Lista de jogos com odds
        """
        if USE_MOCK_DATA:
            logger.info("Usando dados simulados para odds")
            return MOCK_ODDS
        
        try:
            url = f"{self.base_url}/sports/{sport}/odds"
            params = {
                "apiKey": self.api_key,
                "regions": regions,
                "markets": markets,
                "dateFormat": "iso"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            odds = response.json()
            logger.info(f"Obtidas odds para {len(odds)} jogos de {sport}")
            return odds
        except Exception as e:
            logger.error(f"Erro ao obter odds para {sport}: {e}")
            return []
    
    def get_todays_games_and_odds(self, sport="soccer"):
        """
        Obtém jogos e odds para hoje.
        
        Args:
            sport (str): Chave do esporte
            
        Returns:
            tuple: (jogos, odds)
        """
        logger.info(f"Coletando dados para {sport}...")
        
        # Obter jogos
        games = self.get_games(sport)
        
        # Obter odds
        odds = self.get_odds(sport)
        
        # Filtrar jogos de hoje (simplificado para dados simulados)
        if not USE_MOCK_DATA:
            today = datetime.now().date()
            filtered_games = []
            filtered_odds = []
            
            for game in games:
                game_date = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00')).date()
                if game_date == today:
                    filtered_games.append(game)
            
            for odd in odds:
                odd_date = datetime.fromisoformat(odd['commence_time'].replace('Z', '+00:00')).date()
                if odd_date == today:
                    filtered_odds.append(odd)
            
            games = filtered_games
            odds = filtered_odds
        
        logger.info(f"Encontrados {len(games)} jogos e {len(odds)} jogos com odds para hoje")
        return games, odds
    
    def format_games_data(self, games):
        """
        Formata dados de jogos em DataFrame.
        
        Args:
            games (list): Lista de jogos
            
        Returns:
            pd.DataFrame: DataFrame com dados formatados
        """
        formatted_games = []
        
        for game in games:
            try:
                commence_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                
                game_data = {
                    'id': game.get('id'),
                    'sport': game.get('sport_key'),
                    'league': game.get('sport_title'),
                    'home_team': game.get('home_team'),
                    'away_team': game.get('away_team'),
                    'commence_time': game.get('commence_time'),
                    'date': commence_time.strftime("%d/%m/%Y"),
                    'time': commence_time.strftime("%H:%M")
                }
                formatted_games.append(game_data)
            except Exception as e:
                logger.error(f"Erro ao formatar jogo {game.get('id', 'unknown')}: {e}")
                continue
        
        return pd.DataFrame(formatted_games) if formatted_games else pd.DataFrame()
    
    def format_odds_data(self, odds_data):
        """
        Formata dados de odds em dicionário estruturado.
        
        Args:
            odds_data (list): Lista de odds
            
        Returns:
            dict: Dicionário com odds formatadas
        """
        formatted_odds = {}
        
        for game in odds_data:
            try:
                game_id = game.get('id')
                game_key = f"{game.get('home_team')} x {game.get('away_team')}"
                
                formatted_odds[game_key] = {
                    'id': game_id,
                    'commence_time': game.get('commence_time'),
                    'bookmakers': {}
                }
                
                for bookmaker in game.get('bookmakers', []):
                    bookie_name = bookmaker.get('key')
                    formatted_odds[game_key]['bookmakers'][bookie_name] = {}
                    
                    for market in bookmaker.get('markets', []):
                        market_key = market.get('key')
                        formatted_odds[game_key]['bookmakers'][bookie_name][market_key] = {}
                        
                        for outcome in market.get('outcomes', []):
                            outcome_name = outcome.get('name')
                            price = outcome.get('price')
                            formatted_odds[game_key]['bookmakers'][bookie_name][market_key][outcome_name] = price
            except Exception as e:
                logger.error(f"Erro ao formatar odds do jogo {game.get('id', 'unknown')}: {e}")
                continue
        
        return formatted_odds

# Instância global do coletor de dados
data_collector = DataCollector()

def get_todays_games_and_odds(sport="soccer"):
    """
    Função de conveniência para obter jogos e odds de hoje.
    
    Args:
        sport (str): Chave do esporte
        
    Returns:
        tuple: (jogos, odds)
    """
    return data_collector.get_todays_games_and_odds(sport)

