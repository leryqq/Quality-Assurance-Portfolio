# Тест-кейс: "Оплата товара"

||Описание|
| --- | --- |
| ID | #002 |
| Название проекта | "Исходный Код" |
| Версия | versionName = "1.0" |
| Название тест-кейса | Оплата товара на сайте |
| Описание | Проверка функционала оплаты товара на сайте |
| Предусловия | Открыта форма оплаты товара на сайте, поля формы (Email, Телефон, Номер банковской карты, CVC) пустые |
| Тестовые данные | Email: ivan@gmail.com; Телефон +7 800 555 3535; Номер банковской карты: 1111 2222 3333 4444; CVC: 123; Код СМС: 123456 |
| Этапы теста | <ol><li>Ввести в поле "Email" email пользователя из тестовых данных</li><li>Ввести в поле "Телефон" телефон из тестовых данных</li><li>Ввести в поле "Номер банковской карты" номер банковской карты из тестовых данных</li><li>Ввести в поле "CVC" cvc из тестовых данных</li><li>Отметить чек бокс "Согласие с офертой"</li><li>Нажать на кнопку "Оплатить"</li><li>Ввести в поле "Код из СМС" код смс из тестовых данных</li><li>Нажать на кнопку "Подтвердить"</li></ol> |
| Ожидаемый результат | Кнопка "Оплатить" должна быть активной. После успешного ввода данных и нажатия на кнопку "Оплатить", открывается страница с подтверждением операции. После ввода "Код из СМС" и нажатия на кнопку "Подтвердить", появляется уведомление об успешной оплате. Пользователь перенаправляется на главную страницу |
| Фактический результат | (Это поле заполняется после выполнения теста) |
| Статус | 🔃Pending |
| Комментарий | Проверить переход по ссылке "Согласие с офертой" |
