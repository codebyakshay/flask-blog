from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
import time

s = Serializer('bayy')
token = s.dumps({'user_id': 1})
print(token)

for n in range(30):
    try:
        # Check the token's validity on each iteration
        data = s.loads(token, max_age=25)
        user_id = data['user_id']
        print(f'{n} {user_id}')
        time.sleep(1)  # Wait for a second
        
    except SignatureExpired:
        print("The token has expired.")
        break  # Exit the loop if the token has expired
    except BadSignature:
        print("Invalid token.")
        break