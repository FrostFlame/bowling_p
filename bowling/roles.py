from rolepermissions.roles import AbstractUserRole


class Editor(AbstractUserRole):
    available_permissions = {
        'create_news_post': True,
    }