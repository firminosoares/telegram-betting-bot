# Bot de Apostas no Telegram - Railway.app

Este é um bot para o Telegram que coleta jogos do dia, verifica odds de casas de apostas, faz análise estatística simples e envia sugestões de apostas diretamente no Telegram. O bot está configurado para ser hospedado gratuitamente no Railway.app.

## 🚀 Deploy Rápido no Railway.app

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## 📋 Funcionalidades

- **Coleta de jogos do dia**: Busca automática de jogos em diversas ligas
- **Verificação de odds**: Consulta odds de diferentes casas de apostas
- **Análise estatística**: Identifica apostas com valor e calcula probabilidades
- **Sugestões de apostas**: Envia recomendações diretamente no Telegram
- **Interface interativa**: Botões para facilitar a navegação
- **Modo simulação**: Funciona com dados fictícios sem necessidade de API externa

## 🤖 Comandos do Bot

- `/start` - Inicia o bot
- `/apostas` - Mostra sugestões de apostas para hoje
- `/jogos` - Lista os jogos do dia
- `/odds` - Mostra as odds para um jogo específico
- `/status` - Mostra o status atual do bot
- `/refresh` - Atualiza manualmente os dados
- `/ajuda` - Mostra a mensagem de ajuda

## 🛠️ Configuração Manual

### 1. Preparar o Bot do Telegram

1. Acesse o Telegram e procure por **@BotFather**
2. Envie `/newbot` e siga as instruções
3. Copie o **Token de API** gerado

### 2. Deploy no Railway.app

1. Acesse [Railway.app](https://railway.app) e faça login
2. Clique em "New Project" → "Deploy from GitHub repo"
3. Conecte sua conta do GitHub e selecione este repositório
4. Configure as variáveis de ambiente (veja seção abaixo)
5. Clique em "Deploy"

### 3. Configurar Variáveis de Ambiente

No painel do Railway.app, vá em "Variables" e configure:

**Obrigatórias:**
- `TELEGRAM_TOKEN`: Token do seu bot do Telegram
- `BOT_USERNAME`: Nome de usuário do bot (sem @)

**Opcionais:**
- `ODDS_API_KEY`: Chave da API de odds (deixe vazio para usar dados simulados)
- `ADMIN_USER_ID`: ID do usuário administrador
- `USE_MOCK_DATA`: `true` para dados simulados, `false` para dados reais
- `DEFAULT_SPORT`: Esporte padrão (`soccer`)
- `ODDS_REGIONS`: Região das odds (`eu`, `uk`, `us`)
- `DAILY_NOTIFICATION_TIME`: Horário das notificações (`09:00`)

### 4. Configurar Webhook

Após o deploy, acesse a URL do seu projeto e adicione `/set_webhook` ao final:
```
https://seu-projeto.railway.app/set_webhook
```

Faça uma requisição POST para esta URL para configurar o webhook automaticamente.

## 🔧 Desenvolvimento Local

### Pré-requisitos

- Python 3.8+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/telegram-betting-bot-railway.git
cd telegram-betting-bot-railway
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Execute o bot:
```bash
python app.py
```

## 📊 API de Odds

Para usar dados reais de odds, você precisa de uma chave de API da [TheOddsAPI](https://theoddsapi.com/):

1. Crie uma conta gratuita
2. Obtenha sua chave de API
3. Configure a variável `ODDS_API_KEY`
4. Defina `USE_MOCK_DATA=false`

**Nota:** A versão gratuita da API tem limitações de requisições por mês.

## 🔍 Monitoramento

O bot inclui endpoints para monitoramento:

- `GET /`: Status geral do bot
- `GET /health`: Health check
- `POST /webhook`: Endpoint para receber updates do Telegram
- `POST /set_webhook`: Configurar webhook automaticamente

## 📝 Logs

Os logs são exibidos no console do Railway.app. Você pode visualizá-los na seção "Deployments" do seu projeto.

## 🚨 Limitações

- **Railway.app gratuito**: 500 horas de execução por mês
- **API de odds gratuita**: Limitação de requisições por mês
- **Dados simulados**: Não refletem odds reais do mercado

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Fazer commit das mudanças
4. Fazer push para a branch
5. Abrir um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

## 🆘 Suporte

Se você encontrar problemas:

1. Verifique os logs no Railway.app
2. Confirme se as variáveis de ambiente estão corretas
3. Teste o bot localmente primeiro
4. Abra uma issue no GitHub com detalhes do problema

---

**Aviso:** Este bot é apenas para fins educacionais. Aposte com responsabilidade e dentro de suas possibilidades financeiras.

