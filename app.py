from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Wallet, Player
# from logger import logger
from schemas.player_schema import PlayerViewSchema, PlayerPath, PlayerDelSchema, DeletePlayerForm, NewPlayerForm, LoginForm
from schemas.blackjack_schema import BlackjackPath
from schemas.blackjack_schema import BetForm
from schemas.error import ErrorSchema
from service.player_service import PlayerService
from service.blackjack_service import BlackjackService
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, supports_credentials=True,  resources={r"/*": {"origins": "*"}})

home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
player_tag = Tag(name="Player",
                 description="Informações de Player e Wallet")


@app.get('/', tags=[home_tag])
@app.get('/home', tags=[home_tag])
@app.get('/index', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/player/<int:id>', responses={"200": PlayerViewSchema, "404": ErrorSchema})
def get_player_by_id(path: PlayerPath):
    service = PlayerService()
    return service.find_by_id(path.id)


@app.post('/player', responses={"200": PlayerViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_player(form: NewPlayerForm):
    """
    Cria um novo Player
    """
    service = PlayerService()
    return service.create(form)


@app.delete('/player/<int:id>',  responses={"200": PlayerDelSchema, "401": ErrorSchema, "400": ErrorSchema})
def delete_player(path: PlayerPath):
    """
    Deleta um Player
    """
    service = PlayerService()
    return service.delete(path)


@app.put('/player/<int:id>/resetcoins', responses={"200": PlayerViewSchema, "404": ErrorSchema})
def reset_coins(path: PlayerPath):
    service = PlayerService()
    return service.reset_coins(path.id)


@app.post('/login', responses={"200": PlayerViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def login_player(form: LoginForm):
    """
    Simples login para o Player - SEM SENHA
    """
    service = PlayerService()
    return service.login(form)


@app.post('/blackjack/new')
def blackjack_new_game(form: BetForm):
    service = BlackjackService()
    print('COMEçOU')
    response = service.new_game(form)
    return response


@app.get('/blackjack/hit/<int:id>')
def blackjack_hit(path: BlackjackPath):
    service = BlackjackService()
    return service.hit(path)


@app.get('/blackjack/double/<int:id>')
def blackjack_double(path: BlackjackPath):
    service = BlackjackService()
    return service.double(path)


@app.get('/blackjack/stand/<int:id>')
def blackjack_stand(path: BlackjackPath):
    service = BlackjackService()
    return service.stand(path)
