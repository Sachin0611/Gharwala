from django.contrib.auth.tokens import PasswordResetTokenGenerator  
import six  #had to instal django utilis as it was not present in django version greater than 3
class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  
account_activation_token = TokenGenerator()  