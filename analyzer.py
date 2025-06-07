"""
Módulo de Análise Estatística para Apostas
-----------------------------------------
Este módulo contém as funções para análise de odds
e geração de sugestões de apostas.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BettingAnalyzer:
    """Classe para análise de apostas e geração de sugestões."""
    
    def __init__(self, games_data, odds_data):
        """
        Inicializa o analisador com dados de jogos e odds.
        
        Args:
            games_data (pd.DataFrame): DataFrame com dados dos jogos
            odds_data (dict): Dicionário com dados de odds
        """
        self.games_data = games_data
        self.odds_data = odds_data
        
    def calculate_implied_probability(self, odds):
        """
        Calcula a probabilidade implícita de uma odd.
        
        Args:
            odds (float): Valor da odd
            
        Returns:
            float: Probabilidade implícita (0-1)
        """
        return 1.0 / odds if odds > 0 else 0.0
    
    def normalize_probabilities(self, probabilities):
        """
        Normaliza probabilidades para somar 100%.
        
        Args:
            probabilities (list): Lista de probabilidades
            
        Returns:
            list: Probabilidades normalizadas
        """
        total = sum(probabilities)
        return [p / total for p in probabilities] if total > 0 else probabilities
    
    def calculate_market_margin(self, odds_list):
        """
        Calcula a margem da casa de apostas.
        
        Args:
            odds_list (list): Lista de odds do mercado
            
        Returns:
            float: Margem da casa (0-1)
        """
        implied_probs = [self.calculate_implied_probability(odd) for odd in odds_list]
        return sum(implied_probs) - 1.0
    
    def find_value_bets(self, game_odds, threshold=0.05):
        """
        Encontra apostas com valor em um jogo.
        
        Args:
            game_odds (dict): Dados de odds do jogo
            threshold (float): Limite mínimo de valor
            
        Returns:
            list: Lista de apostas com valor
        """
        value_bets = []
        
        for bookie_name, markets in game_odds.get('bookmakers', {}).items():
            for market_key, outcomes in markets.items():
                if market_key == 'h2h':  # Resultado final
                    odds_values = list(outcomes.values())
                    if len(odds_values) >= 3:  # Casa, Empate, Fora
                        # Calcular probabilidades implícitas
                        implied_probs = [self.calculate_implied_probability(odd) for odd in odds_values]
                        normalized_probs = self.normalize_probabilities(implied_probs)
                        
                        # Buscar discrepâncias entre casas de apostas
                        for outcome_name, odds_value in outcomes.items():
                            # Calcular valor esperado simples
                            fair_prob = 1.0 / len(odds_values)  # Probabilidade "justa" simplificada
                            implied_prob = self.calculate_implied_probability(odds_value)
                            
                            if fair_prob > implied_prob + threshold:
                                value = (fair_prob * odds_value) - 1.0
                                if value > 0:
                                    confidence = "Alta" if value > 0.15 else "Média" if value > 0.08 else "Baixa"
                                    value_bets.append({
                                        'bookmaker': bookie_name,
                                        'market': market_key,
                                        'outcome': outcome_name,
                                        'odds': odds_value,
                                        'value': value,
                                        'confidence': confidence
                                    })
        
        return value_bets
    
    def analyze_market_trends(self):
        """
        Analisa tendências de mercado para todos os jogos.
        
        Returns:
            dict: Análise de tendências por jogo
        """
        trends = {}
        
        for game_key, game_odds in self.odds_data.items():
            game_trends = {
                'margins': {},
                'best_odds': {},
                'normalized_probs': {}
            }
            
            # Analisar cada casa de apostas
            for bookie_name, markets in game_odds.get('bookmakers', {}).items():
                for market_key, outcomes in markets.items():
                    if market_key == 'h2h':
                        odds_values = list(outcomes.values())
                        margin = self.calculate_market_margin(odds_values)
                        game_trends['margins'][bookie_name] = margin
                        
                        # Encontrar melhores odds por resultado
                        for outcome_name, odds_value in outcomes.items():
                            if outcome_name not in game_trends['best_odds']:
                                game_trends['best_odds'][outcome_name] = {'odds': odds_value, 'bookmaker': bookie_name}
                            elif odds_value > game_trends['best_odds'][outcome_name]['odds']:
                                game_trends['best_odds'][outcome_name] = {'odds': odds_value, 'bookmaker': bookie_name}
            
            # Calcular probabilidades normalizadas usando as melhores odds
            if game_trends['best_odds']:
                best_odds_values = [data['odds'] for data in game_trends['best_odds'].values()]
                implied_probs = [self.calculate_implied_probability(odd) for odd in best_odds_values]
                normalized_probs = self.normalize_probabilities(implied_probs)
                
                outcome_names = list(game_trends['best_odds'].keys())
                game_trends['normalized_probs'] = dict(zip(outcome_names, normalized_probs))
                game_trends['margin'] = min(game_trends['margins'].values()) if game_trends['margins'] else 0.0
            
            trends[game_key] = game_trends
        
        return trends
    
    def generate_suggestions(self, max_suggestions=5):
        """
        Gera sugestões de apostas baseadas na análise.
        
        Args:
            max_suggestions (int): Número máximo de sugestões
            
        Returns:
            list: Lista de sugestões de apostas
        """
        suggestions = []
        
        for game_key, game_odds in self.odds_data.items():
            # Encontrar apostas com valor
            value_bets = self.find_value_bets(game_odds)
            
            # Adicionar as melhores apostas às sugestões
            for bet in value_bets:
                if len(suggestions) >= max_suggestions:
                    break
                    
                suggestion = {
                    'game': game_key,
                    'market': bet['market'],
                    'outcome': bet['outcome'],
                    'bookmaker': bet['bookmaker'],
                    'odds': bet['odds'],
                    'value': bet['value'],
                    'confidence': bet['confidence'],
                    'reason': f"Aposta com valor de {bet['value']:.2f}"
                }
                suggestions.append(suggestion)
        
        # Ordenar por valor decrescente
        suggestions.sort(key=lambda x: x['value'], reverse=True)
        
        return suggestions[:max_suggestions]
    
    def format_suggestions_message(self, suggestions=None):
        """
        Formata as sugestões em uma mensagem para o Telegram.
        
        Args:
            suggestions (list): Lista de sugestões (opcional)
            
        Returns:
            str: Mensagem formatada
        """
        if suggestions is None:
            suggestions = self.generate_suggestions()
        
        if not suggestions:
            return "Não foram encontradas sugestões de apostas para hoje. 🤔"
        
        today = datetime.now().strftime("%d/%m/%Y")
        message = f"🔮 *Sugestões de Apostas - {today}*\n\n"
        
        for suggestion in suggestions:
            game = suggestion['game']
            market = "Resultado Final" if suggestion['market'] == 'h2h' else suggestion['market']
            outcome = suggestion['outcome']
            
            # Traduzir resultado se necessário
            if suggestion['market'] == 'h2h':
                if outcome == "Draw":
                    outcome = "Empate"
                else:
                    outcome = f"Vitória {outcome}"
            
            odds = suggestion['odds']
            confidence_stars = "⭐⭐⭐" if suggestion['confidence'] == "Alta" else "⭐⭐" if suggestion['confidence'] == "Média" else "⭐"
            
            message += f"⚽ *{game}*\n"
            message += f"📊 Sugestão: {market} - {outcome}\n"
            message += f"💰 Odd: {odds:.2f}\n"
            message += f"🔍 Confiança: {confidence_stars}\n\n"
        
        message += "_Nota: Estas são apenas sugestões baseadas em análise estatística. Aposte com responsabilidade._"
        
        return message

