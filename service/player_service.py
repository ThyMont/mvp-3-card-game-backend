from model.player import Player
from model.wallet import Wallet
from schemas.player_schema import NewPlayerForm, DeletePlayerForm, UpdateWalletForm
from model import Session
from logger import logger
from sqlalchemy.exc import IntegrityError


class PlayerService:

    def find_by_id(_, id: int):
        session = Session()
        player = session.query(Player).filter(Player.id == id).first()
        if not player:
            error_msg = "Player não encontrado:/"
            logger.warning(
                f"Erro ao procurar Player id:{id}, {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.info(f"Player encontrado: {player.username}")
            return {'player': player.to_dict()}, 200

    def create(_, form: NewPlayerForm):
        try:
            player = Player(
                name=form.name, username=form.username, password=form.password)
            session = Session()
            session.add(player)
            session.commit()
            player.create_wallet()
            session.commit()
            print(player)
            return {'player': player.to_dict()}, 200
        except IntegrityError as e:
            # como a duplicidade do usernome é a provável razão do IntegrityError
            error_msg = "Username already used:/"
            logger.warning(
                f"Erro ao adicionar username '{form.username}', {error_msg}")
            return {"message": error_msg}, 409
        except Exception as e:
            print(e)
            msg = "Não foi possível realizar o cadastro"
            logger.warning(
                f"Erro ao criar o Player (name: {form.name}, username: {form.username})")
            return {'msg': msg}, 400

    def delete(_, form: DeletePlayerForm):
        session = Session()
        player = session.query(Player).filter(
            Player.username == form.username, Player.password == form.password).first()
        if not player:
            # Como o usuário já estará logado, conclui-se que o password esteja incorreto
            error_msg = "Password incorreto/"
            logger.warning(
                f"Erro ao tentar apagar Player. username:{form.username}, {error_msg}")
            return {"message": error_msg}, 401
        else:
            try:
                session.query(Wallet).filter(
                    Wallet.player == player.id).delete()
                session.query(Player).filter(
                    Player.username == form.username, Player.password == form.password).delete()
                session.commit()
                logger.info(f"Player excluido: {player.username}")
                return {'username': player.username, 'message': f"Player {player.username} excluído com sucesso"}, 200
            except Exception as e:
                logger.error(f"Erro ao excluir o: {player}: {e}")
                return {'message': "Não foi possível excluir o Player"}, 400

    def reset_coins(_, id: int):
        session = Session()
        player = session.query(Player).filter(Player.id == id).first()
        player.reset_wallet()
        session.commit()
        if not player:
            error_msg = "Player não encontrado:/"
            logger.warning(
                f"Erro ao procurar Player id:{id}, {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.info(f"Reseted Coins: {player.username}")
            return {'player': player.to_dict()}, 200

    def update_coins(_, old, new):
        if (old + new < 0):
            logger.warning("Erro ao atualizar coins")
            raise ValueError(
                "Quantidade de Coins não pode ser inferior a zero 0")
        return old + new

    def update_wallet(self, form: UpdateWalletForm):
        session = Session()
        player: Player = session.query(Player).filter(
            Player.id == form.player_id).first()
        if not player:
            error_msg = "Player não encontrado:/"
            logger.warning(
                f"Erro ao procurar Player id:{id}, {error_msg}")
            return {"message": error_msg}, 404
        try:
            player.wallet.coin_1 = self.update_coins(
                player.wallet.coin_1, form.coin_1)
            player.wallet.coin_5 = self.update_coins(
                player.wallet.coin_5, form.coin_5)
            player.wallet.coin_25 = self.update_coins(
                player.wallet.coin_25, form.coin_25)
            player.wallet.coin_50 = self.update_coins(
                player.wallet.coin_50, form.coin_50)
            player.wallet.coin_100 = self.update_coins(
                player.wallet.coin_100, form.coin_100)
            session.commit()
            logger.info(f"Reseted Coins: {player.username}")
            return {'player': player.to_dict()}, 200
        except ValueError as e:
            logger.error(f"Erro ao atualizar a wallet: {e}")
            return {'message': "Saldo insuficiente"}, 409
