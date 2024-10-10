import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken, Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import requests
import base64
import json
import time
from django.core.cache import cache
import redis
import jwt
from jwt.exceptions import DecodeError
from rest_framework_simplejwt.settings import api_settings
import os
from dotenv import load_dotenv
from django.http import JsonResponse
import datetime
from rest_framework import status

logger = logging.getLogger(__name__)

class CustomUser:
    def __init__(self, user_id):
        self.id = user_id
        self.username = f"user_{user_id}"
        self.is_authenticated = True

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that extends JWTAuthentication.
    This class handles the authentication process using JWT tokens.
    """

    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        """
        Authenticates the request using JWT token.
        
        Args:
            request (HttpRequest): The request object.
            url (str): The URL to send the token for validation.
        
        Returns:
            tuple: A tuple containing the authenticated user and the raw token.
        
        Raises:
            AuthenticationFailed: If the authorization credentials were not provided or the token is invalid.
        """
        if self.url is None:
            self.url = 'http://localhost:8001/jwt/token/verify/'
        header = self.get_header(request)
        if header is None:
            logger.error("Header not provided ")
            raise AuthenticationFailed("Header not provided")

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.error("Authorization credentials were not provided")
            raise AuthenticationFailed("Authorization credentials were not provided")
        
        try:          
            validated_token = token_backend.decode(raw_token, verify=True)
            user_id = validated_token.get('user_id', None)
        except Exception as e:
            logger.error(f"Invalid token: {e}")
            print(f"Invalid token: {e}")
            raise InvalidToken(e) from e
        if not validated_token or user_id is None:
            logger.error("Invalid token or No user ID found.")
            raise InvalidToken("Invalid token or No user ID found.")        
        AppUser = get_user_model()
         # Ensure AppUser is compared correctly
        expected_model = 'auth_n_auth.models.AppUsers'  # Use the full path of the model
        if AppUser.__module__ + '.' + AppUser.__qualname__ != expected_model:
            app_user = CustomUser(user_id)
            request.user = app_user  # Set to user instance, not just ID
            return app_user, raw_token
        else:
            try:
                app_user = AppUser.objects.get(id=user_id)
                request.user = app_user  # Set to user instance, not just ID
                try:
                    authenticated = super().authenticate(request)
                    return authenticated
                except Exception as e:
                    print(f"Error authenticating: {e}")
                    raise AuthenticationFailed("Error authenticating") from e
            except AppUser.DoesNotExist:
                print(f"\nUser with ID {user_id} does not exist")
                logger.error(f"User with ID {user_id} does not exist")
                raise AuthenticationFailed("Invalid user")
            except Exception as e:
                print(f"\nError fetching user: {e}")
                logger.error(f"Error fetching user: {e}")
                raise AuthenticationFailed("Error fetching user") from e        

class TokenUtils:    
    @classmethod
    def get_tokens_for_user_inline(cls, user):
        token = RefreshToken.for_user(user)
        return str(token), str(token.access_token)        
       
    @classmethod
    def get_tokens_for_user(cls, user):
        token_obtain_url = 'http://localhost/user-mngmt/token/'  # take out to env file
        data = {
            'email': user.email,            
            'user_id': user.id,
            # 'emp_id': user.emp_id
        }
        try:
            print(f"Data: {data}")
            response = requests.post(token_obtain_url, data=data)
            print(f"Response: {response}")
            response_data = response.json()
            access_token = response_data.get('access', None)
            refresh_token = response_data.get('refresh', None)
 
            if access_token and refresh_token:
                print (f"No access token: {access_token} and refresh token: {refresh_token}")
                return access_token, refresh_token
            else:
                return None, None
        except Exception as e:
            print(f'Token Obtain Error: {e}')
            return None, None
       
    @classmethod
    def refresh_access_token(cls, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return new_access_token
        except Exception as e:
            print(f'Token Refresh Error: {e}')
            return None
   
    @classmethod
    def verify_token(cls, access_token):
        try:
            token = AccessToken(access_token)
            success, info = token.verify()
            return success, info
        except Exception as e:
            print(f'Token Verify Error: {e}')
            return False, str(e)
         
    @classmethod
    def decode_token(cls, token):
        try:
            # Decode token to inspect the payload without verifying the signature
            verifying_key = api_settings.VERIFYING_KEY
            decoded_token = jwt.decode(token, verifying_key, algorithms=['RS256'], options={"verify_signature": True})            
            return decoded_token
        except jwt.InvalidSignatureError as e:
            print(f"Invalid Signature Error: {e}")
            return None
        except DecodeError as e:
            
            print(f"\nInvalid token: {e}\n=====================\n")
            return None        
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None
   
    @classmethod
    def get_expiry(cls, jwt_token):
        print(F"Inisde get_expiry: {jwt_token}")
        if type(jwt_token) == dict:
            payload = jwt_token.get('exp', None)
            print(f"\nPayload: {payload}")
            return payload
        else:
            payload = jwt_token.split('.')[1]
            # Add padding to fix incorrect token length
            payload += '=' * (-len(payload) % 4)
            decoded_payload = base64.b64decode(payload)
            payload_json = json.loads(decoded_payload)
            return payload_json['exp']
   
    @classmethod
    def is_token_expired(cls, jwt_token):
        expiry = cls.get_expiry(jwt_token)
        check_time = time.time()
        return check_time > expiry
        
    @classmethod
    def validate_token(cls, token):
        try:  
            # Validate token by creating an UntypedToken instance
            decoded_token = cls.decode_token(token)
            generic_token = UntypedToken(token, verify=True)
            verify = generic_token.verify()
            if not decoded_token:
                raise jwt.InvalidSignatureError  
            if verify:
                print(f"Token verified: {verify}")
                raise InvalidToken(verify)   
            if cls.is_token_expired(decoded_token):
                print(f"Token expired: {decoded_token}")
                raise TokenError('Token expired')       
            return True
        except InvalidToken as e:
            print(f"Token validation error: {e}")
            return False
        except TokenError as e:
            print(f"Token error in Validate Token: {e}")
            return False
        except jwt.InvalidSignatureError as e:
            print(f"Invalid Signature Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during token validation: {e}")
            return False
   
    @classmethod
    def create_token(cls, payload):
        try:
            # Create a new token using the payload
            token = jwt.encode({**payload, "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)}, api_settings.SIGNING_KEY, algorithm='RS256')
            return token
        except Exception as e:
            print(f"Error creating token: {e}")
            return None
        
    @classmethod
    def check_blacklist(cls, token, token_type="refresh"):
        blacklist = cls.get_blacklist()
        if not blacklist.get('refresh_tokens', None) and not blacklist.get('access_tokens', None):
            print ("\n\nNo tokens in blacklist\n\n")
            return True
        refresh_tokens = blacklist.get('refresh_tokens', None)  
        access_tokens = blacklist.get('access_tokens', None)
        if token_type == "refresh":
            for r_token in refresh_tokens:
                if r_token == token:
                    return False
        if token_type == "access":
            if isinstance(token, list):
                token = token[0]
            elif isinstance(token, str):
                token = token.split(' ')
                if len(token) > 1:
                    token = token[1]
            for a_token in access_tokens:                
                if a_token == token:
                    return False
        return True
 
    @classmethod
    def get_blacklist(cls):
        url = 'http://127.0.0.1/oauth/jwt/blacklist/all/'        
        try:
            response = requests.get(url)
            response_data = response.json()
            return response_data
        except requests.RequestException as e:
            print(f"Error getting blacklist: {e}")
            return None
    
    