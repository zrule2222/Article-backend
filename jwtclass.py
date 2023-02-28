import jwt
import datetime
from app import app
from models.Article import ArticleModel


class jwtclass:

 def encode_auth_token(self,user_id):
     try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
     except Exception as e:
        return e
        
 def decode_auth_token(self,auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """

    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'  


