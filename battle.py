# import game as game
import random

from db import UserInfo
import sys
from flask import Flask, request, jsonify
import logging

# from db import UserInfo as u_i
# from db import DB as d_b

# db = UserInfo("worlds_War.db")

app = Flask(__name__)
log = logging.basicConfig(level=logging.DEBUG)


# user_info = (application_id, user_id, country_name, xp, army_count, power_score)

# TODO: def defer: return answer and wait for answer
# inp -
# request.j

@app.route('/webhook', methods=['POST'])
def run():
    logging.info(request.json)
    resp = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response':
            {
                'end_session': False
            }
    }

    debug_data = {'F5AD2EE44EF5919E0331D849436A4268A31B5D7A360A0ADC83421C709601709B': 'waiting_for_country_name'}
    main = Main()
    speech = Replicas()

    if request.json['session']['new']:
        debug_data[request.json['session']['application']['application_id']] = "waiting_for_country_name"
        resp['response']['text'] = speech.country_name
        print(resp)
        return jsonify(resp)
    else:
        if debug_data[request.json['session']['application']['application_id']] == "waiting_for_country_name":
            resp['response']['text'] = main.game_start(request.json['request']['command'], request.json)
            print(resp)
            return jsonify(resp)

    if main.debug_data[request.json['session']['application']['application_id']] == 1:
        main.debug_data[request.json['session']['application']['application_id']] = 5

    elif main.debug_data[request.json['session']['application']['application_id']] == 2:
        main.menu()

    elif main.debug_data[request.json['session']['application']['application_id']] == 3:
        main.menu_handler(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 4:
        main.help()

    elif main.debug_data[request.json['session']['application']['application_id']] ==5:
        main.game_start()

    elif main.debug_data[request.json['session']['application']['application_id']] == 6:
        main.user_info()

    elif main.debug_data[request.json['session']['application']['application_id']] == 7:
        main.user_info_handler(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 8:
        main.upgrade()

    elif main.debug_data[request.json['session']['application']['application_id']] == 9:
        main.upgrade_type_handler(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 10:
        main.upgrade_tanks(request=request.json, cost=main.cost)

    elif main.debug_data[request.json['session']['application']['application_id']] == 11:
        main.upgrade_ships(request=request.json, cost=main.cost)

    elif main.debug_data[request.json['session']['application']['application_id']] == 12:
        main.upgrade_soldiers(request=request.json, cost=main.cost)

    elif main.debug_data[request.json['session']['application']['application_id']] == 13:
        main.upgrade_planes(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 14:
        main.matchmaking(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 15:
        main.matchmaking_handler(request=request.json)

    elif main.debug_data[request.json['session']['application']['application_id']] == 16:
        main.battle(compl=main.true_enemy_complexity)

    elif main.debug_data[request.json['session']['application']['application_id']] == 17:
        main.battle_handler_true(request=request.json)




class Answer(object):
    """
    Answer
    """

    def __init__(self, text, requires_answer: bool):
        super(Answer, self).__init__()
        self.text = text
        self.requires_answer = requires_answer

    @property
    def content(self):  #
        """
        Answer content
        :return:
        """
        return self.text

    @property
    def requires_answer(self) -> bool:
        """
        Does Answer requires an answer?
        :return: bool
        """
        return self.requires_answer

    @requires_answer.setter
    def requires_answer(self, value):
        self._requires_answer = value


class Helper:

    @staticmethod
    def defer(answer, req_answer):
        if req_answer == True:
            return Answer(answer, True)

    @staticmethod
    def tactics_sort(level) -> tuple:
        mass = []
        for i in Project.Army.tactics.keys():
            if Project.Army.tactics[i][2] == level:
                mass.append(i)
        return tuple(mass)

    @staticmethod
    def define(tactic_name):
        for k, v in Project.Army.tactics.items():
            if v[0] == tactic_name.lower().strip():
                return k


class Main:
    def __init__(self, stage=1):
        super(Main, self).__init__()
        self.debug_data = {'F5AD2EE44EF5919E0331D849436A4268A31B5D7A360A0ADC83421C709601709B': 'waiting_for_country_name'}
        self.debug_data[request.json['session']['application']['application_id']] = stage
        self.user = User()
        self.speech = Replicas()
        self.countries = Countries()
        self.country_name = self.user.country_name
        self.stage = stage

    def menu(self, stage=2):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        return self.speech.choose_menu

    def menu_handler(self, request, stage=3):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        try:
            user_req = request['request']['command']
            if 'война' in user_req:
                self.matchmaking()
            elif 'прокачка' in user_req or 'прокачки' in user_req:
                self.upgrade()
            elif 'информация' in user_req:
                self.user_info()

            elif 'помощь' in user_req:
                return help()

            else:
                raise Exception('false answer')
        except Exception as e:
            return self.speech.repeat, '\n' + self.speech.choose_menu

    def help(self, stage=4):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        self.stage = 'help'
        return self.speech.user_help + ' \n' + 'Скажите "ВЕРНУТЬСЯ", чтобы вернуться.'

    def chance_percentage(self, *kwargs) -> bool:
        if len(kwargs) == 1:
            res = self.definition_chance(1, 100)
            if res <= int(kwargs[0]):
                return True
            else:
                return False
        else:
            raise Exception(
                '#error1 Количество переданных аргументов не подходит для возвращения результата. (len kwargs != 1)!')

    def definition_chance(self, *args) -> int:
        if len(args) == 2:
            res = random.randint(int(args[0]), int(args[1]))
            return res
        else:
            raise Exception(
                '#error2 Количество переданных аргументов не подходит для возвращения результата. (len kwargs != 2)!')

    def game_start(self, country_name=None, request=None, stage=5):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        if self.debug_data[request.json['session']['application']['application_id']] == 5:
            try:
                self.user.country_name = country_name
                if self.country_name not in Countries().countries_names:
                    self.stage = 2
                    return str(self.speech.country_story(country_name))
            except Exception as e:
                if str(e) == 'country is exist':
                    return (self.speech.country_exist + ' \n' + Replicas().country_name)
                else:
                    return (str(e))
        else:
            try:
                if 'помощь' in request['request']['command']:
                    return help()
                if 'продолжить' in request['request']['command']:
                    self.menu()
                else:
                    raise Exception('False answer')
            except Exception:
                return self.speech.repeat + ' \n' + self.speech.country_story(self.country_name)

        self.menu()

    def user_info(self, command=None, stage=6):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        return (
            f'{self.country_name}, {User().lvl_deter(0)} м. у. ({Countries().Complexity.translation[User().compl_deter(User().lvl_deter(0))]}), численность армии - {self.user.count} чел,\n'
            f'Количество XP  - {self.user.xp}.\n'
            f'Чтобы вернуться скажите "ВЕРНУТЬСЯ".')

    def user_info_handler(self, request, stage=7):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        while True:
            user_req = request['request']['command']
            try:
                if 'вернуться' in user_req or 'вернутся' in user_req:
                    self.menu()
                else:
                    raise Exception('False answer')
            except Exception:
                return (Replicas(self.user).repeat, '\n' + 'Чтобы вернуться скажите "ВЕРНУТЬСЯ".')

            else:
                break

    def upgrade(self, stage=8):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        upg = tuple(self.user.upgrades.values())  # танки, флот, пехота, авиация
        return (f'Уровни прокачки:\n'
                f'Артиллерия: {upg[0]} ур.\n'
                f'Флот: {upg[1]} ур.\n'
                f'Пехота: {upg[2]} ур.\n'
                f'Авиация: {upg[3]} ур.\n'
                f'Для прокачки назовите категорию армии (например: Флот)\n'
                f'Для выхода скажите "ВЕРНУТЬСЯ".\n')

    def upgrade_type_handler(self, request, stage=9):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        user_req = request['request']['command']
        upg = tuple(self.user.upgrades.values())
        try:
            if 'танк' in user_req or 'танки' in user_req or 'артиллерия' in user_req or 'артиллерии' in user_req:
                self.cost = round(20 + (upg[0] * 0.25))
                return (f'Цена: {self.cost} xp, ваш xp {self.user.xp}, вы хотите продолжить? Скажите "ДА" или "НЕТ".')

            elif 'флот' in user_req or 'корабли' in user_req or 'корабль' in user_req or 'морское' in user_req:
                self.cost = round(20 + (upg[1] * 0.25))
                return f'Цена: {self.cost} xp, ваш xp {self.user.xp}, вы хотите продолжить? Скажите "ДА" или "НЕТ".'

            elif 'пехота' in user_req or 'пешие' in user_req or 'люди' in user_req or 'пехоту' in user_req:
                self.cost = round(20 + (upg[2] * 0.25))
                return (f'Цена: {self.cost} xp, ваш xp {self.user.xp}, вы хотите продолжить? Скажите "ДА" или "НЕТ".')

            elif 'самолет' in user_req or 'авиация' in user_req or 'авиацию' in user_req or 'самолеты' in user_req:
                self.cost = round(20 + (upg[3] * 0.25))
                return (f'Цена: {self.cost} xp, ваш xp {self.user.xp}, вы хотите продолжить? Скажите "ДА" или "НЕТ".')

        except Exception as e:
            return str(e)

    def upgrade_tanks(self, request, cost, stage=10):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        try:
            user_req = request['request']['command']
            if 'да' in user_req:
                if self.user.xp >= cost:
                    self.user.xp -= cost
                    self.user.upgrades['tanks'] += 1
                    self.user.lvl_deter(self.user.lvl)
                    self.menu()
                else:
                    self.stage = 'menu'
                    return ('Недостаточно xp! Для того, чтобы вернуться в меню, скажите "МЕНЮ".')

            elif 'нет' in user_req:
                self.menu()
            else:
                raise Exception('false answer!')

        except Exception:
            return Replicas().repeat + ' \n' + 'Скажите "ДА" или "НЕТ".'

    def upgrade_ships(self, request, cost, stage=11):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        while True:
            try:
                user_req = request['request']['command']
                if 'да' in user_req:
                    if self.user.xp >= cost:
                        self.user.xp -= cost
                        self.user.upgrades['fleet'] += 1
                        self.user.lvl_deter(self.user.lvl)
                        self.menu()
                    else:
                        self.stage = 'menu'
                        return ('Недостаточно xp! Для того, чтобы вернуться в меню, скажите "МЕНЮ".')

                elif 'нет' in user_req:
                    self.stage = 'menu'
                    self.menu()
                else:
                    raise Exception('false answer!')

            except Exception:
                return (self.speech.repeat + ' \n' + 'Скажите "ДА" или "НЕТ".')

    def upgrade_soldiers(self, request, cost, stage=12):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        try:
            user_req = request['request']['command']
            if 'да' in user_req:
                if self.user.xp >= cost:
                    self.user.xp -= cost
                    self.user.upgrades['infantry'] += 1
                    self.user.lvl_deter(self.user.lvl)
                    self.menu()
                else:
                    self.stage = 'menu'
                    return ('Недостаточно xp! Для того, чтобы вернуться в меню, скажите "МЕНЮ".')

            elif 'нет' in user_req:
                self.stage = 'menu'
                self.menu()
            else:
                raise Exception('false answer!')

        except Exception:
            return (self.speech.repeat, '\n' + 'Скажите "ДА" или "НЕТ".')

    def upgrade_planes(self, request, stage=13):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        try:
            while True:
                try:
                    user_req = request
                    if 'да' in user_req:
                        if self.user.xp >= self.cost:
                            self.user.xp -= self.cost
                            self.user.upgrades['air_force'] += 1
                            self.user.lvl_deter(self.user.lvl)
                            self.menu()
                        else:
                            yield say('Недостаточно xp! Для того, чтобы вернуться в меню, скажите "МЕНЮ".')
                            while True:
                                try:
                                    user_req = command
                                    if 'меню' in user_req:
                                        self.menu()
                                    else:
                                        raise Exception('false answer')
                                except Exception:
                                    return (self.speech.repeat +
                                            '\n' + 'Для того, чтобы вернуться в меню, скажите "МЕНЮ".')
                                else:
                                    break

                    elif 'нет' in user_req:
                        self.menu()
                        break

                    elif 'помощь' in user_req:
                        return help()

                    elif 'вернутся' in user_req or 'вернуться' in user_req:
                        self.menu()

                    else:
                        raise Exception('false answer!')

                except Exception:
                    return (self.speech.repeat + '\n' + 'Скажите "ДА" или "НЕТ".')

                else:
                    break

        except Exception:
            return (self.speech.repeat +
                    ' \n' + 'Для прокачки назовите категорию армии (например: Флот)\nДля выхода скажите "ВЕРНУТЬСЯ"')

    def matchmaking(self, request, stage=14):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        self.battle_enemy = random.choice(self.countries.countries_names)

        while True:
            try:
                enemy_complexity = request.command
                true_enemy_complexity_index = list(self.countries.Complexity.translation.values()).index(
                    enemy_complexity.title())
                self.true_enemy_complexity = list(self.countries.Complexity.translation.keys())[
                    true_enemy_complexity_index]
            except Exception:
                return (self.speech.repeat + ' \n' + self.speech.enemy_complexity)
            else:
                break

        return (self.speech.tactic(self.battle_enemy))

    def matchmaking_handler(self, request, stage=15):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        while True:
            try:
                tact = request.command  # tact = 'штурм'
                true_tact = Helper.define(tactic_name=tact)
                self.battle(self.true_enemy_complexity, Project.Army.tactics[true_tact])
            except Exception as e:
                return (self.speech.repeat, '\n' + self.speech.tactic(self.battle_enemy))
            else:
                break

    def battle(self, compl, tact, command=None, stage=16):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        complexity_index = random.choice(self.countries.Complexity.complexity_index_levels[compl])
        true_enemy_level = self.countries.Complexity.complexity_index_levels[compl][complexity_index]
        ct = random.randint(true_enemy_level * 20000, true_enemy_level * 75000)
        a, b = self.countries.Complexity.complexeties[compl][complexity_index][0], \
               self.countries.Complexity.complexeties[compl][complexity_index][1]
        c = sorted([a, b])
        def_chance = self.definition_chance(c[0], c[1])
        def_chance += ct // self.user.count + sum(list(self.user.upgrades.values())) // 10 - self.user.power_score / 10
        if self.chance_percentage(tact[1]):
            def_chance += 7
        else:
            def_chance -= 7

        if self.chance_percentage(def_chance):
            xp = 2 + ((100 - def_chance) // 10)
            if xp < 0:
                xp = 2
            self.user.xp, self.user.count = self.user.xp + xp, self.user.count + ct
            self.user.lvl_deter(self.user.lvl)
            self.user.power_score += 5
            return (
                f'Итог: {self.speech.you_won(xp, ct)}\n'
                f'Для того, чтобы продолжить скажите "ПРОДОЛЖИТЬ".\n'
                f'Для того, чтобы завершить игру скажите "ВЫЙТИ".')

        else:
            xp = 2
            ct = self.user.count - self.user.count // 100 * 80
            self.user.xp, self.user.count = self.user.xp + xp, self.user.count + ct
            self.user.lvl_deter(self.user.lvl)
            return (f'{self.speech.battle_story}\n'
                    f'Итог: {self.speech.game_over(xp, ct)}\n'
                    f'Для того, чтобы продолжить скажите "ПРОДОЛЖИТЬ".\n'
                    f'Для того, чтобы завершить игру скажите "ВЫЙТИ".')

    def battle_handler_true(self, request, stage=17):
        self.debug_data[request.json['session']['application']['application_id']] = stage
        while True:
            user_req = request['request']['command']
            try:
                if 'продолжить' in user_req:
                    self.menu()
                elif 'выйти' in user_req or 'выйди' in user_req or 'выход':
                    self.stage = 'quit'
                    return ('До свидания!')
                else:
                    raise Exception('false answer')
            except Exception:
                return (self.speech.repeat, '\n' + f'Для того, чтобы продолжить скажите "ПРОДОЛЖИТЬ"\n.'
                                                   f'Для того, чтобы завершить игру скажите "ВЫЙТИ".')


class Countries:
    countries_names = (
        'Демократическая республика Харито', 'Доруко', 'Тароко', 'Республика Конош', 'Жанвонгская Империя',
        'Захкуп', 'Цуншец', 'Палмро', 'Элтатро', 'Шанко', 'Ферквонгское Королевство', 'Дагенций', 'Пронкист',
        'Южный Жерволингск', 'Северный Жерволингск', 'Восточный Апронг', 'Западный Апронг', 'Стензл',
        'Сегуцская Республика',
        'Митио', 'Выгай', 'Республика Ить', 'Северный Лозниг', 'Центральный Лозниг', 'Лозниг', 'Бонгай', 'Хукстан',
        'Тапроф', 'Республика Харокуя', 'Достуц', 'Астенгам', 'Жазцунг', 'Самдянг', 'Зеншац',
        'Китягн', 'Руспол', 'Лоднег', 'Терлип', 'Средний Додест', 'Республика Выгай', 'Демократическая республика Ить',
        'Лозниг', 'Бонгай', 'Женгостак', 'Опростан', 'Выукстоф', 'Мийцк', 'Тапроф', 'Женпрай', 'Республика Хукстан'
    )

    class Complexity:
        complexeties = {
            'easy': ((68, 70), (57, 60), (52, 40)),
            'middle': ((48, 50), (42, 45), (37, 40)),
            'hard': ((31, 39), (24, 31), (21, 23)),
            'hardcore': ((18, 20), (9, 12), (1, 8)),
        }

        translation = {
            'easy': 'Легкий',
            'middle': 'Средний',
            'hard': 'Сложный',
            'hardcore': 'Хардкорный'
        }

        user_easy = tuple(list(list(complexeties.values())[0]).copy())
        user_middle = tuple(list(list(complexeties.values())[1]).copy())
        user_hard = tuple(list(list(complexeties.values())[2]).copy())
        user_hardcore = tuple(list(list(complexeties.values())[3]).copy())
        complexity_levels = {'easy': (0, 1, 2),
                             'middle': (3, 4, 5),
                             'hard': (6, 7, 8, 9),
                             'hardcore': (10, 11, 12)
                             }
        complexity_index_levels = {'easy': (0, 1, 2),
                                   'middle': (0, 1, 2),
                                   'hard': (0, 1, 2, 3),
                                   'hardcore': (0, 1, 2)
                                   }


class Project:
    # уровень / xp для достижения
    levels = {
        0: 0,
        1: 5,
        2: 20,
        3: 50,
        4: 125,
        5: 315,
        6: 790,
        7: 1975,
        8: 5000,
        9: 10250,
        10: 25625,
        11: 64100,
        12: 160250
    }

    class Army:
        # штурм
        tactics = {
            'assault': ('штурм', 45, 0),
            'counterattack': ('контратака', 47, 0),
            'crankle': ('зигзаг', 49, 1),
            'performance': ('быстродействие', 51, 1),
            'capture': ('захват', 53, 2),
            'interception': ('перехват', 55, 2),
            'espionage': ('шпионаж', 53, 3),
            'silence': ('тишина', 51, 3),
            'deception': ('обман', 54, 4),
            'madness': ('безумие', 37, 4),
            'destruction': ('уничтожение', 49, 5),
            'accuracy': ('аккуратность', 52, 5),
            'benefit': ('польза', 51, 6),
            'pacifism': ('пацифизм', 33, 6),
            'annihilation': ('аннигиляция', 59, 7),
            'cross': ('крест', 41, 7),
            'straight': ('прямая', 52, 8),
            'detour': ('обход', 54, 8),
            'hide-n-seek': ('прятки', 53, 9),
            'thunder': ('гром', 56, 9),
            'partisan': ('партизанская', 54, 10),
            'duplicate': ('дубликат', 50, 10),
            'offensive': ('наступление', 51, 11),
            'parts': ('части', 52, 11),
            'steel': ('сталь', 53, 12),
            'charisma': ('харизма', 54, 12),
            'alienation': ('отчуждение', 54, 12)
        }


class User:
    def __init__(self):
        self.country_name = 'None'
        self.xp = 0
        self.lvl = self.lvl_deter(xp=self.xp)
        self.tactics = Helper.tactics_sort(level=self.lvl)
        self.complexity = self.compl_deter(lvl=self.lvl)
        self.power_score = 0
        self.count = 75000
        self.upgrades = {
            'tanks': 0,
            'fleet': 0,
            'infantry': 0,
            'air_force': 0
        }

    def lvl_deter(self, xp):
        res = []
        for j, k in Project().levels.items():
            if xp >= k:
                res.append(j)
        return res[-1]

    def compl_deter(self, lvl):
        for j, k in Countries.Complexity.complexity_levels.items():
            if lvl in k:
                return j


class Replicas:
    def __init__(self, user: User = None):
        super(Replicas, self).__init__()
        self.user = user

    def country_story(self, name):
        return f'Здравствует наша страна - {name}! Поздравляю вас с тем, что стали главнокомандующим!\n' \
               f'Я буду вашим личным помощником и клянусь, что буду служить вам с совестью и честью.\n' \
               f'Наш народ - великий, а великий народ - это великая армия, так давайте это докажем всему миру!\n' \
               f'Если вы не знаете правила игры - скажите "ПОМОЩЬ", иначе скажите - "ПРОДОЛЖИТЬ".\n'

    @property
    def enemy_complexity(self) -> str:
        complex_index = list(Countries().Complexity.translation.keys()).index(self.user.complexity)
        compl_1 = list(Countries().Complexity.translation.values())[complex_index]
        try:
            compl_2 = list(Countries().Complexity.translation.values())[complex_index + 1]
        except Exception:
            return f'Выберите сложность соперника: {compl_1}'
        else:
            return f'Выберите сложность соперника: {compl_1} или {compl_2}'

    @property
    def country_name(self) -> str:
        return 'Приветствую вас, товарищ! Мне доложили, что вас хотят сдеалать главнокомандующим нашей страны,\n' \
               'Правитель доверяет вам и просит переименовать название страны, чтобы полностью избаиться от\n' \
               'пережитков прошлого. Придумайте название не длинное, но и не короткое. А также, чтобы подобных стран\n' \
               'не было в нашем мире. Подумайте хорошо и назовите, ведь в будущем переименовать страну будет невозможно!\n' \
               'Назовите название страны:'

    @property
    def country_exist(self) -> str:
        return 'Прошу прощения, но страна с таким названием уже существет. Пожалуйста, назовите другое название.'

    def you_won(self, xp, ct):
        return f'Вы победили, поздавляем с победой! +{xp} XP, +{ct} числ.'

    def game_over(self, xp, ct):
        return f'Вы проиграли! +{xp}, -{ct}'

    def tactic(self, enemy) -> str:
        lst = [Project().Army.tactics[x][0].title() for x in self.user.tactics]
        lst = '; '.join(lst)
        return f'Наш враг - {enemy}! Назовите тактику, которая есть в списке: {lst}.'

    @property
    def repeat(self) -> str:
        lst = ['Товарищ главнокомандующий, повторите, пожалуйста!', 'Извините, я вас не понял, повторите пожалуйста!',
               'Смею попросить вас повторить.', 'Товарищ, я вас не совсем понял, что вы сказали?',
               'Прошу вас повторить!',
               'Пожалуйста, повторите, я вас не понял.', 'Повторите, пожалуйста, я не расслышал.',
               'Еще раз повторите, пожалуйста.',
               'Что вы имели в виду?', 'Пожалуйста, ответьте на вопрос. Повторите.']
        return random.choice(lst)

    @property
    def choose_menu(self) -> str:
        return 'Товарищ, скажите, что вы хотите выбрать: война, прокачки, информация о нашей армии, помощь или выход?'

    @property
    def user_help(self) -> str:
        return 'Товарищ, вы знаете, что наша страна - великая. Наша задача - расширить границы и стать главным лидером\n' \
               'на мировой арене. Для этого нам требуется воевать со странами разной сложности. Чем сложнее страна, тем\n' \
               'меньше у нас шансов на победу. После любой войны, вы получаете опыт, который вы можете тратить на прокачку\n' \
               'армии (флот, авиация, пехота, танки) или для прокачки уровня вашей страны на мировой арене. После каждой войны\n' \
               'численность нашей армии или увеличивается, или уменьшается. Это зависит от количества погибших и военнопленных.\n' \
               'Так давайте же уже начнем Великую войну! Скажите "ВЕРНУТЬСЯ", чтобы вернуться.'

    @property
    def battle_story(self) -> str:
        stories = ('В основном битвы проходили кровавые.  Враги пытались в основном атаковать с помощью авиации. \n'
                   'Среди наших солдат было поймано около 1700 предателей, что позор для нас, но тем не менее среди \n'
                   'нас были и отважные воины. Ключевым моментом произошел захват военного вражеского лагеря #17.',)
        return random.choice(stories)

    @property
    def upgrade_help(self) -> str:
        res = 'Тcоварищ, чем больше вы будете прокачивать и улучшать нашу армию, тем выше шанс на победу!\n' \
              'Прокачки покупаются за опыт (XP). Для того, чтобы вернуться скажите "ВЕРНУТЬСЯ".'
        return res

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0', ssl_context='adhoc')
    # status = True
    # while status:
    #     project = Project()
    #     speech = Replicas()
    #     countries = Countries()
    #     user = User()
    #     main = Main()
    #     main.game_start()
