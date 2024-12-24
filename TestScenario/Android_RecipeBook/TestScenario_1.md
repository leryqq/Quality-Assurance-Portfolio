# Тестовый сценарий: «Добавление ингредиентов в список покупок»

### Приоритет тестирования
Normal

### Название теста
Добавление ингредиента в список покупок

### Этапы теста
1.	Запустить приложение.
2.	Войти в учетную запись пользователя, используя валидные данные.
3.	Ввести в поле поиска название существующего рецепта.
4.	Нажать на рецепт.
5.	На странице рецепта у ингредиентов нажать на «+».
6.	Проверить, что появилось сообщение «"Ингредиент" добавлен в список покупок».
7.	Перейти в список покупок.
8.	Проверить наличие в списке ранее добавленных ингредиентов.
9.	Вручную добавить ингредиент, нажав на «+».
10.	Заполнить поле «Название» данными.
11.	Нажать на кнопку «Добавить».
12.	Проверить наличие добавленного вручную продукта.

### Тестовые данные
*	логин: ivanov1234@mail.ru;
*	пароль: ivanov1234;
*	рецепт: «Томатный суп-пюре»;
*	продукт: «Помидор - 500г».

### Ожидаемый результат
Добавленные ингредиенты в список покупок со страницы рецепта и продукты добавленные вручную

### Фактический результат
Ингредиенты со страницы рецепта корректно добавляются в список покупок. Функция добавления продукта вручную также успешно работает