from datetime import date

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.db.models import Q

SEX_CHOICES = (
    ('0', 'Женский'),
    ('1', 'Мужской')
)


class UserManager(BaseUserManager):
    """Определяем менеджер для модели User без поля username"""
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с заданными email и паролем"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создает и сохраняет суперюзера с заданными email и паролем"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractUser):
    # Убираем неиспользуемые поля
    username = None
    first_name = None
    last_name = None
    is_photographer = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(null=False, default=False)
    # Вместо username используем email
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()
    REQUIRED_FIELDS = []


class PlayerManager(models.Manager):
    def get_similar_players(self, primary_player):
        """
        Находит игроков, регистрационные данные которого совпадают с принимаемым.

        Args:
            primary_player (PlayerInfo): игрок, по которому находим похожих.

        Returns:
            Если имеются похожие игроки, то возвращает их queryset, иначе возвращает None.
        """
        try:
            similar_players = PlayerInfo.objects.filter(Q(i_name__icontains=primary_player.i_name) &
                                                        Q(f_name__icontains=primary_player.f_name) &
                                                        Q(o_name__icontains=primary_player.o_name) &
                                                        Q(date_of_birth__exact=primary_player.date_of_birth) &
                                                        ~Q(pk=primary_player.pk))
        except PlayerInfo.DoesNotExist:
            similar_players = None

        return similar_players

    def get_players_by_license_type(self, license_type):
        if license_type.name == 'Спортивный':
            players = PlayerInfo.objects.filter(license__iregex='\\d+').values('id', 'f_name', 'i_name', 'o_name')
        else:
            players = PlayerInfo.objects.all().values('id', 'f_name', 'i_name', 'o_name')
        return players


class PlayerInfo(models.Model):
    class Meta:
        verbose_name_plural = 'Игроки'

    f_name = models.CharField(max_length=50, blank=False)
    i_name = models.CharField(max_length=50, blank=False)
    o_name = models.CharField(max_length=50, blank=True)

    date_of_birth = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')
    phone = models.CharField(max_length=15, blank=True, default='Не указан')

    city = models.ForeignKey('City')
    category = models.ForeignKey('SportCategory')
    license = models.CharField(max_length=20, blank=True, default='Не указана')

    email = models.EmailField(blank=True, default='')

    objects = PlayerManager()

    def __str__(self):
        return f'{self.f_name} {self.i_name} {self.o_name}'

    def fullName_lower(self):
        return '{0} {1} {2}'.format(self.f_name.lower(), self.i_name.lower(), self.o_name.lower())

    def get_age(self):
        today = date.today()
        x = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def get_team(self, tournament, type):
        teams = self.team.filter(tournament=tournament, type=type)
        for team in teams:
            if self in team.players.all():
                return team


class SportCategory(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Спортивные разряды'


class City(models.Model):
    name = models.CharField(max_length=60, default='Не указан')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Города'
