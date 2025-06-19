from .models import ProPlayer, User

class AuthHandler:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.errors = list()
    
    def authenticate(self):
        print(self.username, self.password)
        user = User.objects.filter(username=self.username).first()
        if user: 
            if user.check_password(self.password):
                return user
            else: 
                self.errors.append('wrong password')
                return None
        self.errors.append('wrong handle')
        return None
    

            

