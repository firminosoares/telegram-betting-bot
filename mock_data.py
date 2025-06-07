"""
Dados simulados para desenvolvimento e testes
-------------------------------------------
Este módulo contém dados fictícios de jogos e odds
para permitir o funcionamento do bot sem APIs externas.
"""

from datetime import datetime, timedelta

# Gerar data para hoje e amanhã
today = datetime.now()
tomorrow = today + timedelta(days=1)

# Dados simulados de jogos
MOCK_GAMES = [
    {
        "id": "game_001",
        "sport_key": "soccer_epl",
        "sport_title": "Premier League",
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "commence_time": today.strftime("%Y-%m-%dT%H:%M:%SZ")
    },
    {
        "id": "game_002", 
        "sport_key": "soccer_epl",
        "sport_title": "Premier League",
        "home_team": "Chelsea",
        "away_team": "Arsenal",
        "commence_time": today.strftime("%Y-%m-%dT%H:%M:%SZ")
    },
    {
        "id": "game_003",
        "sport_key": "soccer_laliga",
        "sport_title": "La Liga",
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "commence_time": tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ")
    },
    {
        "id": "game_004",
        "sport_key": "soccer_serie_a",
        "sport_title": "Serie A",
        "home_team": "Juventus",
        "away_team": "AC Milan",
        "commence_time": tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ")
    },
    {
        "id": "game_005",
        "sport_key": "soccer_bundesliga",
        "sport_title": "Bundesliga",
        "home_team": "Bayern Munich",
        "away_team": "Borussia Dortmund",
        "commence_time": tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
]

# Dados simulados de odds
MOCK_ODDS = [
    {
        "id": "game_001",
        "sport_key": "soccer_epl",
        "sport_title": "Premier League",
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "commence_time": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bookmakers": [
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Manchester United", "price": 2.50},
                            {"name": "Liverpool", "price": 3.20},
                            {"name": "Draw", "price": 3.50}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 1.75},
                            {"name": "Under 2.5", "price": 2.20}
                        ]
                    }
                ]
            },
            {
                "key": "betfair",
                "title": "Betfair",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Manchester United", "price": 2.40},
                            {"name": "Liverpool", "price": 3.10},
                            {"name": "Draw", "price": 3.60}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 1.80},
                            {"name": "Under 2.5", "price": 2.15}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "id": "game_002",
        "sport_key": "soccer_epl",
        "sport_title": "Premier League", 
        "home_team": "Chelsea",
        "away_team": "Arsenal",
        "commence_time": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bookmakers": [
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Chelsea", "price": 2.10},
                            {"name": "Arsenal", "price": 3.00},
                            {"name": "Draw", "price": 3.40}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 2.20},
                            {"name": "Under 2.5", "price": 1.70}
                        ]
                    }
                ]
            },
            {
                "key": "unibet",
                "title": "Unibet",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Chelsea", "price": 2.05},
                            {"name": "Arsenal", "price": 3.10},
                            {"name": "Draw", "price": 3.30}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 2.25},
                            {"name": "Under 2.5", "price": 1.65}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "id": "game_003",
        "sport_key": "soccer_laliga",
        "sport_title": "La Liga",
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "commence_time": tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bookmakers": [
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Real Madrid", "price": 2.40},
                            {"name": "Barcelona", "price": 3.20},
                            {"name": "Draw", "price": 3.00}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 1.90},
                            {"name": "Under 2.5", "price": 1.95}
                        ]
                    }
                ]
            },
            {
                "key": "betfair",
                "title": "Betfair",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Real Madrid", "price": 2.35},
                            {"name": "Barcelona", "price": 3.30},
                            {"name": "Draw", "price": 2.95}
                        ]
                    },
                    {
                        "key": "totals",
                        "outcomes": [
                            {"name": "Over 2.5", "price": 1.85},
                            {"name": "Under 2.5", "price": 2.00}
                        ]
                    }
                ]
            }
        ]
    }
]

