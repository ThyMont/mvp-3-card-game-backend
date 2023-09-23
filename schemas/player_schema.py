from pydantic import BaseModel, Field
from model import Player


class WalletViewSchema(BaseModel):
    coin_1 = 5
    coin_5 = 4
    coin_25 = 5
    coin_50 = 5
    coin_100 = 1
    total = 500


class PlayerViewSchema(BaseModel):
    """
    Apresentação do Player. A Wallet apresenta a quantidade de cada Coin e o valor total das Coins
    """
    id: int = 1
    name: str = 'Sam Oak'
    username: str = 'sammy'
    wallet: WalletViewSchema


def print_player(player: Player):
    return player.to_dict()


class PlayerPath(BaseModel):
    """
    Recupera o ID do Player
    """
    id: int = Field(1, description='ID do Player')


class NewPlayerForm(BaseModel):
    """
    Formulário de criação de novo player
    """
    name: str
    username: str


class LoginForm(BaseModel):
    """
    Formulário de login - SEM SENHA
    """
    username: str


class DeletePlayerForm(BaseModel):
    """
    Formulário para exclusão de novo player
    """
    player_id: int


class PlayerDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    username: str
