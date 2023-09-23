from pydantic import BaseModel, Field


class BlackjackPath(BaseModel):
    """
    Recupera o ID da partida
    """
    id: int = Field(1, description='ID da partida')


class BetForm(BaseModel):
    """
    Aposta do Player
    """
    player_id: int = Field(1, description='ID do Player')
    coin_1: int = Field(0, description='Quantidade de Coins 1', include=0)
    coin_5: int = Field(0, description='Quantidade de Coins 5', include=0)
    coin_25: int = Field(0, description='Quantidade de Coins 25', include=0)
    coin_50: int = Field(0, description='Quantidade de Coins 50', include=0)
    coin_100: int = Field(0, description='Quantidade de Coins 100', include=0)
