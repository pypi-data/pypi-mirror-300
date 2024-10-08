# Instagram Web Auth

Авторизация в Instagram через web схему.

## Не поддерживается:

- 2FA
- восстановление доступа

## Example:

```python
from instagram_auth.service.WebLoginService import WebLoginService

service = WebLoginService()

async def main():
    user, session_id = await service.login(username="", password="")    

```

# Внимание

> Автор/ы кода не несут ответственности если ваш аккаунт заблокируют или получит ограничения
