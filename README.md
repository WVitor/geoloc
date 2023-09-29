# geoloc-api
 
**Configurações de Ambiente virtual** 
- Windows: `/.venvWindows/Scripts/activacte`
- Linux `source ./venvLinux/bin/activate`

**Gerar um requirements.txt para atualizar as dependências do projeto (caso necessário)**
dentro do ambiente virtual selecionado execute `pip install -r requirements.txt` ou `pip3 install -r requirements.txt` caso seja python3

**Configurando variáveis de ambiente**
- Crie um arquivo `.env` e inclua as seguintes variáveis de ambientes e seus valores
- `WEATHER_KEY=<valor da variável>`, key para a api do weather api.
- `MAPS_KEY=<valor da variável>`, key para a api do github
- `JWT_SECRET=<valor da variavel`, secret da jwt

**Execução em produção**
- Windows: `waitress-serve --listen=*:5000 main:app`
- Linux: `gunincorn --bind 0.0.0.0:5000 main:app` ou `gunicorn main:app`