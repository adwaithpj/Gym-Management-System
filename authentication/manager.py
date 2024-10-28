from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self,username, phone_number,password=None,**extra_fields):
        if not username:
            raise ValueError('username must be specified')
        if not phone_number:
            raise ValueError('Phone number must be provided')
        email = extra_fields.pop('email', None)
        if email:
            extra_fields['email'] = str(self.normalize_email(email))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using =self._db)
        
        return user
        
    def create_superuser(self, username,phone_number, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        

        return self.create_user(username,phone_number, password, **extra_fields)
        