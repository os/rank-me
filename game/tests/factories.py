from django.contrib.auth import get_user_model
import factory


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')
