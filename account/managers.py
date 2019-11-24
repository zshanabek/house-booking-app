from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


class UserManager(BaseUserManager):

    def create_user(self, email, phone, gender, first_name, last_name, birth_day, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            birth_day=birth_day
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, gender, first_name, last_name, birth_day, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            birth_day=birth_day
        )

        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
