#!/usr/bin/env python3
"""
Script de teste para verificar se o bot está funcionando corretamente
"""

import sys
import os
import asyncio
import logging

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collector import DataCollector
from analyzer import BettingAnalyzer
from config import TELEGRAM_TOKEN, USE_MOCK_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_data_collection():
    """Testa a coleta de dados."""
    logger.info("Testando coleta de dados...")
    
    collector = DataCollector()
    
    # Testar obtenção de jogos e odds
    games, odds = collector.get_todays_games_and_odds()
    
    if games and odds:
        logger.info(f"✅ Coleta de dados OK - {len(games)} jogos, {len(odds)} jogos com odds")
        return True
    else:
        logger.error("❌ Falha na coleta de dados")
        return False

async def test_analysis():
    """Testa a análise estatística."""
    logger.info("Testando análise estatística...")
    
    try:
        collector = DataCollector()
        games, odds = collector.get_todays_games_and_odds()
        
        if not games or not odds:
            logger.error("❌ Não há dados para análise")
            return False
        
        games_df = collector.format_games_data(games)
        odds_dict = collector.format_odds_data(odds)
        
        analyzer = BettingAnalyzer(games_df, odds_dict)
        suggestions = analyzer.generate_suggestions(max_suggestions=3)
        
        if suggestions:
            logger.info(f"✅ Análise estatística OK - {len(suggestions)} sugestões geradas")
            return True
        else:
            logger.warning("⚠️ Análise OK mas nenhuma sugestão gerada")
            return True
    except Exception as e:
        logger.error(f"❌ Erro na análise: {e}")
        return False

def test_config():
    """Testa as configurações."""
    logger.info("Testando configurações...")
    
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN não configurado")
        return False
    
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_TOKEN":
        logger.error("❌ TELEGRAM_TOKEN não foi alterado do valor padrão")
        return False
    
    logger.info(f"✅ Configurações OK - Modo simulação: {USE_MOCK_DATA}")
    return True

async def main():
    """Função principal de teste."""
    logger.info("Iniciando testes do Bot de Apostas no Telegram...")
    
    tests = [
        ("Configurações", test_config),
        ("Coleta de dados", test_data_collection),
        ("Análise estatística", test_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testando {test_name} ---")
        
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        
        results.append(result)
        
        if result:
            logger.info(f"✅ {test_name}: PASSOU")
        else:
            logger.error(f"❌ {test_name}: FALHOU")
    
    # Resumo dos resultados
    logger.info("\n--- RESUMO DOS TESTES ---")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        logger.info(f"🎉 Todos os testes passaram! ({passed}/{total})")
        logger.info("O bot está pronto para deploy!")
        return 0
    else:
        logger.error(f"❌ {total - passed} teste(s) falharam. ({passed}/{total})")
        logger.error("Corrija os problemas antes do deploy.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

