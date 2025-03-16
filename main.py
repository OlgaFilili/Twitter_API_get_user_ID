import os
import tweepy
import requests
import datetime
import time
import logging
from dotenv import load_dotenv
from urllib import parse
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s: %(message)s'
logging.basicConfig(filename='main.log', level=logging.INFO, format=FORMAT)
logger.info("Let's log!")

#   Using OAuth 2.0 Authorization Code with PKCE authentication methods.
#   All information that needed for authorization and liking tweet
#   read from .env-file from script`s directory.
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_uri= os.getenv("REDIRECT_URI")
scopes=os.getenv("SCOPES")
auth_uri= os.getenv("AUTH_URI")
token_uri= os.getenv("TOKEN_URI")

#   Modification Tweepy`s Oauth2UserHandler to save code_verifier.
#   Code_verifier generated for authorization.
#   Used for getting access_token further.
class NotTweepyOAuth2UserHandler(OAuth2Session):
    def __init__(
        self, client_id: str, client_secret: str, redirect_uri: str, scope: list[str], code_verifier: str | None = None
    ):
        super().__init__(client_id, redirect_uri=redirect_uri, scope=scope)
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.code_verifier = code_verifier or str(self._client.create_code_verifier(128))

    def get_authorization_url(self) -> str:
        url, state_seems_unnecessary = self.authorization_url(
            auth_uri,
            code_challenge=self._client.create_code_challenge(self.code_verifier, "S256"),
            code_challenge_method="S256",
        )
        return url

#   For authorization url-code_verifier should be generated.
#   For exchanging code on the access_token- using generated before code_verifier. 
def _oauth2_handler(callback_url: str, code_verifier: str | None) -> tweepy.OAuth2UserHandler:
    return NotTweepyOAuth2UserHandler(
        CLIENT_ID,
        CLIENT_SECRET,
        callback_url,
        ["tweet.read", "users.read"],
        code_verifier=code_verifier,
    )

def get_twitter_authorize_url_and_verifier(callback_url: str) -> tuple[str, str]:
    handler = _oauth2_handler(callback_url, None)
    authorize_url = handler.get_authorization_url()
    return authorize_url, handler.code_verifier               

#   Request to like the tweet.
def like_the_tweet(u_id,tweet_to_like, token):
        retries = 3
        retry_codes = [500, 502, 503, 504] # INTERNAL_SERVER_ERROR, BAD_GATEWAY, SERVICE_UNAVAILABLE, GATEWAY_TIMEOUT
        rate_limits_code= 429 # TOO_MANY_REQUESTS
        
        url = "https://api.x.com/2/users/{}/likes".format(u_id)
        payload = {"tweet_id": tweet_to_like}
        headers = {
            "Authorization": "Bearer "+token,
            "Content-Type": "application/json"
        }
        date1 = datetime.datetime.today()
        print(date1.strftime('%d-%m-%Y %H:%M:%S'))

        
        for n in range(retries):
            try:
                response = requests.request("POST", url, json=payload, headers=headers)

                logger.info("The moment of truth! Response status code is:")
                logger.info(response.status_code)
                response.raise_for_status()
                logger.info("The tweet was liked successfully.")
                logger.info("---------------------------------")
                print("The tweet was liked successfully.")
                break
            except:
                if response.status_code==rate_limits_code:
                    logger.error(f"ERROR!!! {response.text}")
                    #print(f"Error: {response.text}")

                    reset_time = int(response.headers.get("x-rate-limit-reset"))
                    #print (response.headers.get("x-rate-limit-reset"))
                    current_time = int(time.time())
                    wait_time = max(reset_time - current_time, 0)
                    logger.info("Rate limit exceeded. Retry after {} seconds.".format((n+1)*wait_time))
                    print(f"Rate limit exceeded. Retry after {(n+1)*wait_time} seconds.")
##                    if (n==retries-1):
##                         logger.info("Unsuccessfull execution:(. The tweet wasn`t liked.")
##                         logger.info()
##                         print("Unsuccessfull execution:(. The tweet wasn`t liked.")
##                    
                    #   Retry after growing intervals according to attempt number
                    time.sleep((n+1)*wait_time)
                    continue
                if response.status_code in retry_codes:
                    print(f"Error: {response.text}")
                    logger.error(f"ERROR!!! {response.text}")
                    logger.info("Retry after {} seconds.".format((n+1)*10))
                    print(f"Retry after {(n+1)*10} seconds.")
                    time.sleep((n+1)*10)
                    continue
                    
                response.raise_for_status()
            finally:
                if (n==retries-1):
                         logger.info("Unsuccessfull execution:(. The tweet wasn`t liked.")
                         logger.info("--------------------------------------------------")
                         print("Unsuccessfull execution:(. The tweet wasn`t liked.")
                
            raise
def get_user_id(token):
    url="https://api.x.com/2/users/me"
    headers = {
            "Authorization": "Bearer "+token}
    while True:
            response = requests.request("GET", url, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                    response.status_code, response.text
                    )
                )
                return response.status_code
            
            logger.info(response.json())
            return response.json()['data']['id']
      
authorization_url, code_verifier= get_twitter_authorize_url_and_verifier(redirect_uri)
logger.info("Have got an authorization URL:")
logger.info(authorization_url)
print("Log in using the link: {}".format(authorization_url))

#   Authorization URL can be used for authorizing the app.
#   Once they have done so, they would be redirected to the Redirect URL with state and code providing.
verifier = input("Paste the Redirect URL here: ")

#   Save the code to get the access token.
params_code = dict(parse.parse_qsl(parse.urlsplit(verifier).query))
logger.debug("Code for exchanging on access token (from redirect URL): {}".format(params_code['code']))

#   Request to get access token.
headers_at = {'Content-Type': 'application/x-www-form-urlencoded'}
response_at = requests.post(token_uri, data={
    'grant_type': 'authorization_code',
    'client_id':CLIENT_ID,
    'redirect_uri': redirect_uri,
    'code': params_code['code'],
    'code_verifier': code_verifier
    }, headers= headers_at)

logger.info("Response status code for access token request is:")
logger.info(response_at.status_code)

if response_at.status_code != 200:
    logger.error(f"ERROR!!! {response_at.text}")
    print(f"Error: {response.text}")
else:
    #print(response_at.json())
    access_token = response_at.json()['access_token']

    logger.info("Have got an access token.")
    #print("Have got an access token")
    logger.info("Let`s know more about user!")
    #like_the_tweet(USER_ID, tweet_to_like_ID, access_token)
    user_ID=get_user_id(access_token)
    logger.info("Get user_ID (and even more) successfully!")
