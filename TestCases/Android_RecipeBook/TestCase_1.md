# Тест-кейс: «Регистрация в приложении»

||Описание|
| --- | --- |
| Название проекта | RecipeBook |
| Версия | versionName = "1.0" |
| Название тест-кейса | Регистрация нового пользователя |
| Описание | Проверка функционала входа зарегистрированного пользователя в информационную систему |
| Предусловия | Мобильное приложение запущено |
| Тестовые данные | Пользователь Ivanov с почтой ivanov1234@mail.ru и паролем ivanov1234, также с согласием с политикой конфиденциальности |
| Этапы теста | <ol><li>На странице авторизации перейти в раздел «Регистрация»</li><li>В соответствующие поля ввести данные пользователя: Ivanov, почта: ivanov1234@mail.ru, пароль: ivanov1234, отмечен флажок «Соглашаюсь с Политикой конфиденциальности»</li><li>Нажать на кнопку «Создать».</li><li>Сообщение об успешной регистрации «Вы успешно зарегистрировались!»</li></ol> |
| Ожидаемый результат | Создание учетной записи пользователя и перенаправление на страницу авторизации |
| Фактический результат | После ввода и подтверждения данных создается учетная запись пользователя с перенаправлением на страницу авторизации |
| Статус | ✅Passed |
| Комментарий | Имеются проверки на наличие пустых полей |