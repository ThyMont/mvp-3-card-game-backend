from model.player import Player
from model.match import Match
from model import Session


def validate_bet(player_id, coin_1, coin_5, coin_25, coin_50, coin_100):
    if coin_1 + coin_5 + coin_25 + coin_50 + coin_100 == 0:
        return 'APOSTA_ZERADA'
    session = Session()
    player = session.query(Player).filter(Player.id == player_id).first()
    if not player:
        return 'PLAYER NÃO ENCONTRADO'
    if player.wallet.coin_1 < coin_1 or player.wallet.coin_5 < coin_5 or player.wallet.coin_25 < coin_25 or player.wallet.coin_50 < coin_50 or player.wallet.coin_100 < coin_100:
        return 'APOSTA MAIOR DO QUE A QUANTIDADE DE MOEDAS DISPONÍVEL'

    player.wallet.coin_1 = player.wallet.coin_1 - coin_1
    player.wallet.coin_5 = player.wallet.coin_5 - coin_5
    player.wallet.coin_25 = player.wallet.coin_25 - coin_25
    player.wallet.coin_50 = player.wallet.coin_50 - coin_50
    player.wallet.coin_100 = player.wallet.coin_100 - coin_100
    session.commit()
    return 'OK'


def calc_bet(coin_1, coin_5, coin_25, coin_50, coin_100):
    bet_value = (coin_1 * 1) + (coin_5 * 5) + (coin_25 * 25) + \
        (coin_50 * 50) + (coin_100 * 100)
    return bet_value


def pay_bets(match: Match, is_natural):
    bet_value = calc_bet(match.bet_1, match.bet_5,
                         match.bet_25, match.bet_50, match.bet_100)
    if is_natural:
        payment = int(bet_value) * 1.5  # Paga 3:2 em um blackjack natural
    else:
        payment = int(bet_value)  # Paga 1:1 para outras vitórias
    session = Session()
    player = session.query(Player).filter(Player.id == match.player_id).first()

    # Calcular o pagamento em moedas
    player.wallet.coin_100 += payment // 100,
    player.wallet.coin_50 += (payment % 100) // 50,
    player.wallet.coin_25 += ((payment % 100) % 50) // 25,
    player.wallet.coin_5 += (((payment % 100) % 50) % 25) // 5,
    player.wallet.coin_1 += (((payment % 100) % 50) % 25) % 5
    session.commit()
    return payment
