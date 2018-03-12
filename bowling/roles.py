from rolepermissions.roles import AbstractUserRole

class Redactor(AbstractUserRole):
    available_permissions = {
        'create_news_post': True,
    }