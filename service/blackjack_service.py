from model import Session
from model.match import Match
from model.player import Player
from schemas.blackjack_schema import BetForm, BlackjackPath
from sqlalchemy import desc
from logger import logger
from model.utils import validate_bet, pay_bets
import arrow
import math

from dotenv import load_dotenv
import requests
import os

PARTIDA_NAO_ENCONTRADA = "Partida não encontrada"


class BlackjackService():

    def __init__(self):
        load_dotenv()
        self.URL_BLACKJACK = os.getenv('URL_BLACKJACK')

    def new_game(self, form: BetForm):
        validate_msg = validate_bet(form.player_id, form.coin_1,
                                    form.coin_5, form.coin_25, form.coin_50, form.coin_100)
        if validate_msg != 'OK':
            return {'message': validate_msg}, 400

        session = Session()
        url = self.URL_BLACKJACK
        last_match: Match = session.query(Match).filter(Match.player_id ==
                                                        form.player_id).order_by(desc(Match.date)).first()

        new_match = Match()
        new_match.player_id = form.player_id
        new_match.bet_1 = form.coin_1
        new_match.bet_5 = form.coin_5
        new_match.bet_25 = form.coin_25
        new_match.bet_50 = form.coin_50
        new_match.bet_100 = form.coin_100

        if not last_match:
            url += '/newgame'
        else:
            a = arrow.get(last_match.date).date()
            b = arrow.now().date()
            delta = b-a
            if (delta.days) > 14:
                url += '/newgame'
            else:
                url += f"/restart/{last_match.deck_id}"
            if not last_match.game_over:
                last_match.game_over = True
                session.commit()

        request = requests.get(url)
        json = request.json()
        new_match.deck_id = json['deck_id']
        session.add(new_match)
        session.commit()

        return {'match_id': new_match.id,
                'player_id': new_match.player_id,
                'player': json['player'],
                'dealer': json['dealer'],
                'remaining': json['remaining']
                }, 200

    def hit(self, path: BlackjackPath):
        session = Session()
        match = session.query(Match).filter(Match.id == path.id).first()

        if not match:
            return {'message': PARTIDA_NAO_ENCONTRADA}, 404

        url = self.URL_BLACKJACK + '/hit/' + match.deck_id

        request = requests.get(url)
        json = request.json()

        if json['game_over'] == True:
            match.game_over = True
            session.commit()
            if json['winner'] == 'player':
                is_natural = json['is_natural_blackjack']
                payment = pay_bets(match, is_natural)
                return {'match_id': match.id,
                        'player_id': match.player_id,
                        'player': json['player'],
                        'dealer': json['dealer'],
                        'payment': payment,
                        'game_over': True,
                        'winner': json['winner'],
                        'remaining': json['remaining']
                        }, 200
            else:
                return {'match_id': match.id,
                        'player_id': match.player_id,
                        'player': json['player'],
                        'dealer': json['dealer'],
                        'game_over': True,
                        'winner': json['winner'],
                        'remaining': json['remaining']
                        }, 200

        return {'match_id': match.id,
                'player_id': match.player_id,
                'player': json['player'],
                'dealer': json['dealer'],
                'remaining': json['remaining']
                }, 200

    def double(self, path: BlackjackPath):
        session = Session()
        match = session.query(Match).filter(Match.id == path.id).first()

        if not match:
            return {'message': PARTIDA_NAO_ENCONTRADA}, 404

        url = self.URL_BLACKJACK + '/double/' + match.deck_id

        request = requests.get(url)
        json = request.json()

        match.game_over = True
        session.commit()
        if json['winner'] == 'player':
            is_natural = json['is_natural_blackjack']
            payment = pay_bets(match, is_natural)
            return {'match_id': match.id,
                    'player_id': match.player_id,
                    'player': json['player'],
                    'dealer': json['dealer'],
                    'payment': payment,
                    'game_over': True,
                    'winner': json['winner'],
                    'remaining': json['remaining']
                    }, 200
        else:
            return {'match_id': match.id,
                    'player_id': match.player_id,
                    'player': json['player'],
                    'dealer': json['dealer'],
                    'game_over': True,
                    'winner': json['winner'],
                    'remaining': json['remaining']
                    }, 200

    def stand(self, path: BlackjackPath):
        session = Session()
        match = session.query(Match).filter(Match.id == path.id).first()

        if not match:
            return {'message': PARTIDA_NAO_ENCONTRADA}, 404

        url = self.URL_BLACKJACK + '/stand/' + match.deck_id

        request = requests.get(url)
        json = request.json()

        match.game_over = True
        session.commit()
        if json['winner'] == 'player':
            is_natural = json['is_natural_blackjack']
            payment = pay_bets(match, is_natural)
            return {'match_id': match.id,
                    'player_id': match.player_id,
                    'player': json['player'],
                    'dealer': json['dealer'],
                    'payment': payment,
                    'game_over': True,
                    'winner': json['winner'],
                    'remaining': json['remaining']
                    }, 200
        else:
            return {'match_id': match.id,
                    'player_id': match.player_id,
                    'player': json['player'],
                    'dealer': json['dealer'],
                    'game_over': True,
                    'winner': json['winner'],
                    'remaining': json['remaining']
                    }, 200
