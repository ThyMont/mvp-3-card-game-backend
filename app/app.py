from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Wallet, Player
# from logger import logger
from schemas import *
from service import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

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


@app.delete('/player',  responses={"200": PlayerDelSchema, "401": ErrorSchema, "400": ErrorSchema})
def delete_player(form: DeletePlayerForm):
    """
    Deleta um Player
    """
    service = PlayerService()
    return service.delete(form)


@app.put('/player/<int:id>/resetcoins', responses={"200": PlayerViewSchema, "404": ErrorSchema})
def reset_coins(path: PlayerPath):
    service = PlayerService()
    return service.reset_coins(path.id)
