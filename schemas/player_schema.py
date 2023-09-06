from pydantic import BaseModel, Field
from model import Player, Wallet


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
    password: str


class DeletePlayerForm(BaseModel):
    """
    Formulário para exclusão de novo player
    """
    username: str
    password: str


class PlayerDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    username: str


class UpdateWalletForm(BaseModel):
    """
    Adiciona ou remove Coins. Valores positivos para adicionar e negativos para remover.
    0 ou não incluir o parâmetro não altera o objeto
    """
    player_id: int
    coin_1: int = 0
    coin_5: int = 0
    coin_25: int = 0
    coin_50: int = 0
    coin_100: int = 0
    ...
