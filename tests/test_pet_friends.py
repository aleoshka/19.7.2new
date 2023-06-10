from api import PetFriends
from setings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Петя', animal_type='кот', age='14', pet_photo='cat.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

     Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

     # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Петя-петя", "кот", "99", "cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

     # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Петя 2.0', animal_type='кошка', age=19):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


###################################
#     Ещё 10 различных тестов     #
###################################


# 1
def test_add_new_pet_simple_with_valid_data(name='Петя-сим', animal_type='кот', age='2'):
    """Проверяем что можно добавить питомца в упрощенном формате (без фото) с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 2
def test_add_photo_to_pet_with_valid_data(pet_photo='cat.jpeg'):
    """Проверяем что можно добавить фотографию к ранее добавленному питомцу"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Петя-без-фото", "кот", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'pet_photo' in result


# 3
def test_get_api_key_for_incorrect_email(email=valid_email + 'qwerty', password=valid_password):
    """ Проверяем что запрос api ключа с неправильным e-mail'ом возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


# 4
def test_get_api_key_for_incorrect_password(email=valid_email, password=valid_password + 'qwerty'):
    """ Проверяем что запрос api ключа с неправильным паролем возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


# 5
def test_get_api_key_with_empty_email(email='', password=valid_password):
    """ Проверяем что запрос api ключа с пустым e-mail'ом возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


# 6
def test_get_api_key_with_empty_password(email=valid_email, password=''):
    """ Проверяем что запрос api ключа с пустым паролем возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


# 7
def test_get_api_key_with_shuffle_email_password(email=valid_password, password=valid_email):
    """ Проверяем что запрос api ключа с перепутанными e-mail'ом и паролем возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


# 8
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос своих питомцев (при их наличии) возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     # Получаем ключ auth_key и запрашиваем список своих питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, my_pets = pf.get_list_of_pets(auth_key, filter)
#
#     # Проверяем - если список своих питомцев пуст, то добавляем нового и опять запрашиваем список своих питомцев
#     if len(my_pets['pets']) == 0:
#         pf.add_new_pet_simple(auth_key, 'Петр', 'кошка', '2')
#         _, my_pets = pf.get_list_of_pets(auth_key, filter)
#
#     status, result = pf.get_list_of_pets(auth_key, filter)
#
#     assert status == 200
#     assert len(result['pets']) > 0
#
#
# # 9
# def test_get_pets_list_with_incorrect_filter(filter='qwerty'):
#     """ Проверяем что запрос питомцев c некорректным значением поля filter возвращает ошибку.
#     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
#     запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     # Получаем ключ auth_key и запрашиваем список питомцев с неправильным фильтром
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     status, result = pf.get_list_of_pets(auth_key, filter)
#
#     assert status == 500
#     assert 'Filter value is incorrect' in result
#
#
# # 10
# def test_get_my_pets_list_with_invalid_auth_key(filter='my_pets'):
#     """ Проверяем что запрос списка питомцев с неверным auth_key выдаёт ошибку.
#     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее дублируем этого ключ
#     запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     # Получаем ключ auth_key, портим его и запрашиваем список питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     auth_key['key'] += 'qwerty'
#     status, result = pf.get_list_of_pets(auth_key, filter)
#
#     assert status == 403
#     assert 'Please provide &#x27;auth_key&#x27; Header' in result
#
#
# # 11
# def test_get_all_pets_list_with_invalid_auth_key(filter=''):
#     """ Проверяем что запрос списка питомцев с неверным auth_key выдаёт ошибку.
#     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее дублируем этого ключ
#     запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     # Получаем ключ auth_key, портим его и запрашиваем список питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     auth_key['key'] += 'qwerty'
#     status, result = pf.get_list_of_pets(auth_key, filter)
#
#     assert status == 403
#     assert 'Please provide &#x27;auth_key&#x27; Header' in result
#
#
# # 12
# def test_add_new_pet_with_symbols_in_name_type(name='>>#/$|?_(!]{}((~$', animal_type='[:[)%~^|?$%^$:(=%)', age='999', pet_photo='test.jpeg'):
#     """Проверяем что можно добавить питомца со спецсимволами в имени и типе
#      (раз не указанно что нельзя, значит должно быть можно)"""
#
#     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
#     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#
#     # Запрашиваем ключ api и сохраняем в переменную auth_key
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # Добавляем питомца
#     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
#
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 200
#     assert result['name'] == name
#     assert result['animal_type'] == animal_type
#
#
# # 13
# def test_add_new_pet_with_str_in_age(name='Петька', animal_type='кошкин', age='Стар',
#                                      pet_photo='cat.jpeg'):
#     """Проверяем что нельзя добавить питомца с не числовым значением возраста,
#      в API указано что принимает только number"""
#
#     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
#     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#
#     # Запрашиваем ключ api и сохраняем в переменную auth_key
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # Добавляем питомца
#     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
#
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 200
# #    assert result['age'] == age