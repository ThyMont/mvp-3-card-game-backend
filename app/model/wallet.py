from model.base import Base
from sqlalchemy import Column, Integer, ForeignKey


class Wallet(Base):
    """
    Wallet representa a carteira do jogador. Ela armazena as fichas que o jogador possui.
    Por default, cada jogador inicia com um total de $ 500 em fichas
    """
    __tablename__ = 'wallet'
    player = Column(Integer, ForeignKey("player.pk_player"),
                    nullable=False, primary_key=True)

    coin_1 = Column(Integer, default=5)
    coin_5 = Column(Integer, default=4)
    coin_25 = Column(Integer, default=5)
    coin_50 = Column(Integer, default=5)
    coin_100 = Column(Integer, default=1)

    def __init__(self, player_id):
        """
        Cria uma carteira associada a um player
        """
        self.player = player_id

    def reset(self):
        self.coin_1 = 5
        self.coin_5 = 4
        self.coin_25 = 5
        self.coin_50 = 5
        self.coin_100 = 1

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Produto.
        """
        return {
            "coin_1": self.coin_1,
            "coin_5": self.coin_5,
            "coin_25": self.coin_25,
            "coin_50": self.coin_50,
            "coin_100": self.coin_100,
            "total": self.coin_1 * 1 + self.coin_5 * 5 + self.coin_25 * 25 + self.coin_50 * 50 + self.coin_100 * 100
        }

    def update_wallet(self, coin_1=None, coin_5=None, coin_25=None, coin_50=None, coin_100=None):
        """
        Atualiza as informações da Wallet.
        """
        if coin_1 != None:
            self.coin_1 = coin_1
        if coin_5 != None:
            self.coin_5 = coin_5
        if coin_25 != None:
            self.coin_25 = coin_25
        if coin_50 != None:
            self.coin_50 = coin_50
        if coin_100 != None:
            self.coin_100 = coin_100

    def __repr__(self):
        """
        Retorna uma representação da Wallet em forma de texto.
        """
        return f"Wallet(coin_1={self.coin_1}, coin_5={self.coin_5}, coin_25={self.coin_25}, coin_50={self.coin_50}, coin_100={self.coin_100})"
