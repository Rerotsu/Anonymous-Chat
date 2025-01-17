# Анонимный чат

### 1. Введение

Проект представляет собой анонимный чат, где пользователи могут общаться друг с другом без необходимости раскрывать свою личность. Чат будет включать функции регистрации, подтверждения учетных данных и возможность создания как обычных, так и групповых чатов.

### 2. Функционал

 ### 2.1 Регистрация и авторизация
• Пользователь при заходе на любую страницу не авторизованным должен быть перенаправлен на страницу логина/регистрации.
• Регистрация включает форму с полями:
```
  • Email (обязательное, уникальное)
  • Номер телефона (обязательное, уникальное)
  • Пароль (обязательное)
  • Подтверждение пароля (обязательное)
```
• После регистрации данные пользователя сохраняются в БД

• После успешной регистрации пользователь перенаправляется на основную страницу сервиса.

• На основной странице появляется окно для подтверждения почты, где пользователь вводит код, отправленный на его email.

• После подтверждения почты пользователь подтверждает номер телефона аналогичным образом.

### 2.2 Основной интерфейс

• После подтверждения всех данных пользователю открывается доступ ко всем функциям (кроме админских).

• Основная страница выполнена в темных тонах и содержит:

  • В верхнем левом углу отображается надпись "Пользователь - user.id".

  • Центральный блок для чата.

  • Две кнопки:
  
    • "Найти обычный чат (2 человека)"

    • "Найти групповой чат (4 человека)"

### 2.3 Поиск чатов

• При нажатии на "Найти обычный чат" пользователь переходит в состояние "поиска", и создается чат с случайным пользователем, который также находится в состоянии "поиска".

• Интерфейс обычного чата:
```
  • В верхней части отображается "User  - (id собеседника)".
  • Справа от плашки три кнопки: "пожаловаться", "новый чат", "выйти из чата".
  • Ниже располагается область чата с полем ввода сообщения и кнопкой отправки.
```
### 2.4 Групповой чат

• Групповой чат аналогичен обычному, но в верхней части добавляется виджет "Пользователи".

• При наведении на виджет открывается список всех участников чата.

• Справа добавляется кнопка "выгнать участника", которая активируется по голосованию остальных участников чата.

### 3. Технические требования

• Язык программирования: Python

• Используемый фреймворк: FastAPI

• База данных: PostgreSQL

• Интерфейс: HTML/CSS

### 4. Безопасность

• Все пароли должны храниться в зашифрованном виде.

• Необходимореализовать защиту от SQL-инъекций и XSS-атак.

• Подтверждение email и телефона должно включать токены для повышения безопасности.
