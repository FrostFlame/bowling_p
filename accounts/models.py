from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models import Q

from accounts.utils import filename

SEX_CHOICES = (
    ('0', 'Мужской'),
    ('1', 'Женский')
)


# CATEGORY_CHOICES = (
#     ('NONE', 'Нет'),
#     ('3JUN', '3 юношеский'),
#     ('2JUN', '2 юношеский'),
#     ('1JUN', '1 юношеский'),
#     ('3ADU', '3 взрослый'),
#     ('2ADU', '2 взрослый'),
#     ('1ADU', '1 взрослый'),
#     ('KMS', 'Кандидат в мастера спорта'),
#     ('MS', 'Мастер спорта'),
#     ('MSI', 'Мастер спорта международного класса')
# )


class UserManager(BaseUserManager):
    # todo write docs in russian
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
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
    # Remove unused fields
    username = None
    first_name = None
    last_name = None
    email_confirmed = models.BooleanField(null=False, default=False)
    # Using email as username
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS


class PlayerManager(models.Manager):
    # todo rewrite filters
    def get_similar_players(self, primary_player):
        similar_players = PlayerInfo.objects.filter(Q(i_name__icontains=primary_player.i_name) &
                                                    Q(f_name__icontains=primary_player.f_name) &
                                                    Q(o_name__icontains=primary_player.o_name) &
                                                    Q(date_of_birth__exact=primary_player.date_of_birth) &
                                                    ~Q(pk=primary_player.pk) &
                                                    Q(user=None))

        return similar_players


class PlayerInfo(models.Model):
    user = models.OneToOneField(User, null=True, unique=True, related_name="profile")
    license = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey('SportCategory')
    passport = models.ImageField(upload_to=filename)

    # todo add FIAS to database
    city = models.CharField(max_length=30, default='Не указан', blank=True)

    i_name = models.CharField(max_length=50, blank=False)
    f_name = models.CharField(max_length=50, blank=False)
    o_name = models.CharField(max_length=50, blank=True)

    date_of_birth = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')
    phone = models.CharField(max_length=15, blank=True)

    objects = PlayerManager()

    def update(self, obj):
        # Объединяет игрока созданного ранее модератором и игрока, который зарегистрирован пользователем

        # Изменяем внешний ключ user существующего игрока на user нового
        user = obj.user
        obj.user = None
        obj.save()
        self.user = user

        # Обновляем остальные поля
        self.license = obj.license
        self.category = obj.category
        self.passport = obj.passport
        self.city = obj.city
        self.sex = obj.sex
        self.phone = obj.phone
        self.save()


class RegistrationRequestManager(models.Manager):
    def create_request(self, user):
        request = self.create(user=user)
        return request

    def get_active_requests(self):
        return super().get_queryset().filter(status=RegistrationRequest.IN_PROGRESS)


class RegistrationRequest(models.Model):
    IN_PROGRESS = 0
    ACCEPTED = 1
    DECLINED = 2

    REQUEST_STATUS = (
        (IN_PROGRESS, "In progress"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined")
    )

    user = models.OneToOneField(User)
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default=IN_PROGRESS)

    objects = RegistrationRequestManager()


class SportCategory(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
