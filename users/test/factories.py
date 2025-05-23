
import factory
from users.models import CustomUser as UserModel
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class UserCreationFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    is_provider = False
    is_administrador_dcc = True
    is_staff = True
    is_active = True
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())

    class Meta:
        model = UserModel
