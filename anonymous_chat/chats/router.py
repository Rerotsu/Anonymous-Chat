from collections import deque
from fastapi import APIRouter, Query, WebSocket
from anonymous_chat.chats.crypto import encrypt, generate_key
from anonymous_chat.chats.dao import ChatDAO

router = APIRouter(
    prefix="",
    tags=["Чат"]
)

waiting_users = deque()  # Очередь пользователей, ожидающих чат
active_connections = {}


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, user_id: int = Query(...)):
    print(user_id)
    print('0000000000')
    await websocket.accept()
    key = generate_key()  # Генерация ключа один раз при подключении
    waiting_users.append(websocket)  # Добавляем пользователя в очередь
    active_connections[websocket] = user_id
    print('111111111')
    if len(waiting_users) >= 2:
        user1_ws = waiting_users.popleft()
        user2_ws = waiting_users.popleft()
        print("1/5.1/5.1/5")
        user1_id = active_connections[user1_ws]
        user2_id = active_connections[user2_ws]
        print("2222222222222")
        chat_id = await ChatDAO.create_chat_for_users(user1_id, user2_id)
        await user1_ws.send_text(f"You are now in chat {chat_id}")
        await user2_ws.send_text(f"You are now in chat {chat_id}")
        print('333333333333333')
        # Основной цикл для обработки сообщений
        while True:
            try:
                data = await user1_ws.receive_text()
                encrypted_message = encrypt(data, key)
                await user2_ws.send_text(f"Пользователь 1: {encrypted_message}")

                data = await user2_ws.receive_text()
                encrypted_message = encrypt(data, key)
                await user1_ws.send_text(f"Пользователь 2: {encrypted_message}")

            except Exception as e:
                print("Ошибка", e)
                break
