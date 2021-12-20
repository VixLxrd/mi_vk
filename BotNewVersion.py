# -*- coding: utf8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import sqlite3

TOKEN = "760ade263e48296d6369bcfb97317111661d84e14f2e4df2d49f21582ce3b732e850de17e3c32bb968da6"
gr_id = 192948763
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(us_id):  # добавление нового пользователя в бд
    t = 'INSERT INTO members(id, step, name, date, mail, phone, sch, city, class) VALUES(' + str(
        us_id) + ', 0, 0, 0, 0, 0, 0, 0, 0)'
    cursor.execute(t)
    conn.commit()


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    def get_name(uid: int) -> str:
        data = vk.users.get(user_ids=uid)[0]
        return "{}".format(data["first_name"])

    longpoll = VkBotLongPoll(vk_session, gr_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                text = event.obj.message['text']
                vk = vk_session.get_api()
                name = get_name(event.obj.message['from_id'])
                us_id = event.obj.message['from_id']
                if vk.groups.isMember(group_id=gr_id, user_id=us_id):
                    result = cursor.execute(
                        """SELECT step FROM members WHERE id=""" + str(event.obj.message['from_id'])).fetchall()
                    if len(result) == 0:
                        db_table_val(us_id)
                        if text.lower() == 'момент настал':
                            t = "UPDATE members SET\nstep = 1\nWHERE id=" + str(us_id)
                            cursor.execute(t)
                            conn.commit()
                            vk.messages.send(user_id=us_id,
                                             message="😎Итак, мы поняли, что ты настроен(-а) решительно🙃\n\nЧтобы продолжить, надо правильно написать ответ на простой вопрос. Напиши дату основного дня голосования за поправки в Конституцию Российской Федерации\n\nУверены, что тебе не нужно выполнять этот запрос в интернете. Ты и сам(-а) все очень хорошо знаешь!😌",
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button("Момент настал")
                            keyboard = keyboard.get_keyboard()
                            vk.messages.send(user_id=us_id,
                                             message="А теперь напиши: Момент настал",
                                             keyboard=keyboard,
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        step = result[0][0]
                        if step == 0:
                            if text.lower() == 'момент настал':
                                t = "UPDATE members SET\nstep = 1\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                vk.messages.send(user_id=us_id,
                                                 message="😎Итак, мы поняли, что ты настроен(-а) решительно🙃\n\nЧтобы продолжить, надо правильно написать ответ на простой вопрос. Итак, напишите дату основного дня голосования за поправки в Конституцию Российской Федерации\n\nУверены, что тебе не нужно выполнять этот запрос в интернете. Ты и сама все очень хорошо знаешь!😌",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Момент настал")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="А теперь напиши: Момент настал",
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 1:
                            if text in ['01.07.2020', '1.07.2020', '1 июля 2020', '01.07.20', '1.07.20']:
                                t = "UPDATE members SET\nstep = 2\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Регистрация на конкурс")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="Урааа, ты правильно ответил(-а)! Мы в тебе не сомневались😏Наконец-то момент истины настал!\n\nИтак, {}, ты бы хотел(-а) зарегестрироваться на конкурс?".format(
                                                     name),
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=us_id,
                                                 message="Неправильно :( Попробуй ввести ответ в формате ЧЧ.ММ.ГГГГ",
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 2:
                            if text.lower() == "регистрация на конкурс":
                                t = "UPDATE members SET\nstep = 3\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Начать")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 Здравствуй, {}!\n\nТебя приветствует исскуственный интеллект образовательного проекта \"Момент истины\"!\n\nМеня зовут Афина, очень рада знакомству!😄\n\nПри регистрации участника прошу указывать достоверные данные.\n\nГотов(-а) начать?".format(
                                                     name),
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Регистрация на конкурс")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="Итак, {}, ты бы хотел(-а) зарегестрироваться на конкурс?".format(
                                                     name),
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 3:
                            if text.lower() == 'начать':
                                t = "UPDATE members SET\nstep = 4\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Даю свое согласие")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="Согласно ФЗ от 27.07.06 № 152-ФЗ, даю свое согласие на обработку моих персональных данных любым не запрещенным законом способом.\n\nДля того чтобы подтвердить все выше описанное нажмите на кнопку:\nДаю свое согласие",
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Начать")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 Здравствуй, {}!\n\nТебя приветствует исскуственный интеллект образовательного проекта \"Момент истины\"!\n\nМеня зовут Афина, очень рада знакомству!😄\n\nПри регистрации участника прошу указывать достоверные данные.\n\nГотов(-а) начать?".format(
                                                     name),
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 4:
                            if text.lower() == 'даю свое согласие':
                                t = "UPDATE members SET\nstep = 5\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 {}, пожалуйста, введи своё настоящее ФИО.\n\nПример: Иванов Иван Иванович".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Даю Свое Согласие")
                                keyboard = keyboard.get_keyboard()
                                vk.messages.send(user_id=us_id,
                                                 message="Согласно ФЗ от 27.07.06 № 152-ФЗ, даю свое согласие на обработку моих персональных данных любым не запрещенным законом способом.\n\nДля того чтобы подтвердить все выше описанное нажмите на кнопку:\nДаю свое согласие",
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 5:
                            t = "UPDATE members SET\nstep = 6\nWHERE id=" + str(us_id)
                            cursor.execute(t)
                            conn.commit()
                            t = "UPDATE members SET\nname = '{}'\nWHERE id={}".format(text, us_id)
                            cursor.execute(t)
                            conn.commit()

                            vk.messages.send(user_id=us_id,
                                             message="🤖{}, пожалуйста, введи свою дату рождения.\n\nПример 31.01.2003".format(
                                                 name),
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 6:
                            s = text.split('.')
                            try:
                                if len(s) == 3 and 1 <= int(s[0]) <= 31 and 1 <= int(s[1]) <= 12 and 0 <= int(
                                        s[2]) <= 2021:
                                    t = "UPDATE members SET\nstep = 7\nWHERE id=" + str(us_id)
                                    cursor.execute(t)
                                    conn.commit()
                                    t = "UPDATE members SET\ndate = '{}'\nWHERE id={}".format(text, us_id)
                                    cursor.execute(t)
                                    conn.commit()

                                    vk.messages.send(user_id=us_id,
                                                     message="🤖 {}, пожалуйста, введи адрес своей электронной почты.\n\nПример: ivanivanov@mail.ru".format(
                                                         name),
                                                     random_id=random.randint(0, 2 ** 64))
                                else:
                                    blin = 0 / 0
                            except:
                                vk.messages.send(user_id=us_id,
                                                 message="🤖{}, пожалуйста, введи свою дату рождения.\n\nПример 31.01.2003".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 7:
                            try:
                                if text.index('@') >= 0 and text.index('.') >= 0:
                                    t = "UPDATE members SET\nstep = 8\nWHERE id=" + str(us_id)
                                    cursor.execute(t)
                                    conn.commit()
                                    t = "UPDATE members SET\nmail = '{}'\nWHERE id={}".format(text, us_id)
                                    cursor.execute(t)
                                    conn.commit()

                                    vk.messages.send(user_id=us_id,
                                                     message="🤖 {}, пожалуйста, введи свой номер телефона.\n\nПример: +79536061463".format(
                                                         name),
                                                     random_id=random.randint(0, 2 ** 64))
                                else:
                                    blin = 0 / 0
                            except:
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 {}, пожалуйста, введи адрес своей электронной почты.\n\nПример: ivanivanov@mail.ru".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 8:
                            text.replace(' ', '')
                            if ('+' in text and len(text) == 12) or (len(text) == 11):
                                t = "UPDATE members SET\nstep = 9\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                t = "UPDATE members SET\nphone = '{}'\nWHERE id={}".format(text, us_id)
                                cursor.execute(t)
                                conn.commit()

                                vk.messages.send(user_id=us_id,
                                                 message="🤖 {}, пожалуйста, введи наименование своего образовательного учереждения.\n\nПример: МАОУ СОШ №117".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 {}, пожалуйста, введи свой номер телефона.\n\nПример: +79536061463".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 9:
                            t = "UPDATE members SET\nstep = 10\nWHERE id=" + str(us_id)
                            cursor.execute(t)
                            conn.commit()
                            t = "UPDATE members SET\nsch = '{}'\nWHERE id={}".format(text, us_id)
                            cursor.execute(t)
                            conn.commit()

                            vk.messages.send(user_id=us_id,
                                             message="🤖 {}, пожалуйста, введи название населенного пункта, в котором находится твоё образовательное учереждение.\n\nПример: Екатеринбург".format(
                                                 name),
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 10:
                            t = "UPDATE members SET\nstep = 11\nWHERE id=" + str(us_id)
                            cursor.execute(t)
                            conn.commit()
                            t = "UPDATE members SET\ncity = '{}'\nWHERE id={}".format(text, us_id)
                            cursor.execute(t)
                            conn.commit()

                            vk.messages.send(user_id=us_id,
                                             message="🤖 {}, пожалуйста, введи номер и литеру класса, в котором учишься/курс, на котором учишься.\n\nПример: 10Н".format(
                                                 name),
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 11:
                            t = "UPDATE members SET\nstep = 12\nWHERE id=" + str(us_id)
                            cursor.execute(t)
                            conn.commit()
                            t = "UPDATE members SET\nclass = '{}'\nWHERE id={}".format(text, us_id)
                            cursor.execute(t)
                            conn.commit()
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button("Сохранить результаты")
                            keyboard.add_button("Заполнить заново")
                            keyboard = keyboard.get_keyboard()
                            vk.messages.send(user_id=us_id,
                                             message="""🤖 {}, большое спасибо за заполнение анкеты.\n\nСохранить результаты или заполнить заново?""".format(
                                                 name),
                                             keyboard=keyboard,
                                             random_id=random.randint(0, 2 ** 64))

                        elif step == 12:
                            if text == 'Заполнить заново':
                                t = "UPDATE members SET\nstep = 5\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                vk.messages.send(user_id=us_id,
                                                 message="🤖 {}, пожалуйста, введи своё настоящее ФИО.\n\nПример: Иванов Иван Иванович".format(
                                                     name),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                t = "UPDATE members SET\nstep = 13\nWHERE id=" + str(us_id)
                                cursor.execute(t)
                                conn.commit()
                                result = cursor.execute(
                                    """SELECT * FROM members WHERE id=""" + str(
                                        event.obj.message['from_id'])).fetchall()
                                r = list(result[0])
                                vk.messages.send(user_id=us_id,
                                                 message="{}, большое спасибо за заполнение анкеты.\nИтоговые результаты:\n\nФИО: {}\nДата рождения: {}\nНаселенный пункт: {}\nОбразовательное учреждение: {}\nКласс: {}\nEmail: {}\nТелефон : {}\n\n{}, твоя заявка принята!\n\nТеперь для участия в основном конкурсе пройди отборочный тур.\n\nСсылка на отборочный тур:\n\nhttps://forms.gle/Mmm5oHTCg6u4A5GK8\n\nУдачи тебе, {}!😉\n🤖Твоя личная помощница, исскуственный интеллект \"Афина\"".format(
                                                     name, r[2], r[3], r[7], r[6], r[8], r[4], r[5], name, name),
                                                 random_id=random.randint(0, 2 ** 64))

                        elif step == 13:
                            pass

                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Ты до сих пор не подписан(-а) на нашу группу!?😱\nИсправь эту оплошность и заходи обратно в чат 🤖",
                                     random_id=random.randint(0, 2 ** 64))
            except:
                text = event.obj.message['text']
                vk = vk_session.get_api()
                us_id = event.obj.message['from_id']
                vk.messages.send(user_id=208366273,
                                 message="ОШИБКА!! id=" + us_id + " " + text,
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=us_id,
                                 message="🤥 Произошла ошибка :( Скоро мы ее исправим. По всем вопросам: https://vk.com/pskobx",
                                 random_id=random.randint(0, 2 ** 64))

        if event.type == VkBotEventType.GROUP_JOIN:
            result = cursor.execute(
                """SELECT step FROM members WHERE id=""" + str(event.obj.user_id)).fetchall()
            if len(result) == 0:
                db_table_val(event.obj.user_id)
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.user_id,
                             message="Подписался, так держать!\nА теперь напиши: Момент настал",
                             random_id=random.randint(0, 2 ** 64))


while True:
    try:
        if __name__ == '__main__':
            main()
    except:
        pass
