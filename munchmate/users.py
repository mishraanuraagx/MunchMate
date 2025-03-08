from django.contrib.auth.models import User

users = [["user1", "afsrieun123@", "user1@mail"], ["user2", "afqrweeun1a23$", "user2@mail"]]

for user in users:
    if not User.objects.filter(username=user[0]).exists():
        user_obj = User.objects.create_user(user[0], user[2], user[1])
        user_obj.save()
