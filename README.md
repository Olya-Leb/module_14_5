# module_14_5
Задача "Регистрация покупателей";
Цель: написать простейшие CRUD функции для взаимодействия с базой данных;

Дополните файл crud_functions.py:

initiate_db дополните созданием таблицы Users. Эта таблица должна содержать следующие поля:

id - целое число, первичный ключ;
username - текст (не пустой);
email - текст (не пустой);
age - целое число (не пустой);
balance - целое число (не пустой);

add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
1. Кнопки главного меню дополните кнопкой "Регистрация".
2. Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
3. Создайте цепочку изменений состояний RegistrationState.
