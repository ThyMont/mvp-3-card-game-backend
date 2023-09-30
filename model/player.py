from model.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date

from model.wallet import Wallet


class Player (Base):
    '''
    Player representa o jogador. Contém informações como seu ID, nome
    '''

    __tablename__ = 'player'
    id = Column("pk_player", Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)

    wallet = relationship('Wallet', uselist=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        """
        Retorna uma representação do Player em forma de texto.
        """
        return f"Player(id={self.id}, name='{self.name}', username='{self.username}', wallet={self.wallet.__repr__()})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'wallet': self.wallet.to_dict()
        }

    def update_name(self, name):
        self.name = name

    def create_wallet(self):
        self.wallet = Wallet(self.id)

    def reset_wallet(self):
        self.wallet.reset()
