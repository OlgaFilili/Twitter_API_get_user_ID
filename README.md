# Twitter_API_get_user_ID
Try to submit my own project
*	For main.py python-script to get information about an authenticated user.
*	An executor need to have personal account in X with access to developer-account.
*	Installed packages:

tweepy, requests, requests-oathlib, python-dotenv, urllib3

*	All data for authorization and procedure are in .env-file in scripts-directory. Example of the file:

#Provide the consumer key and secret
API_KEY = "ysadfaffsfddf0Y2ih2UJ4"
API_SECRET = "5IAMGD20HvsadfasdfsdfsdwBq2aueMISVFoKnMYrAVQadUxAJEUI"

#Provide client_ID and client secret
CLIENT_ID= "UTsadfas34nV0RFI6MTpjaQ"
CLIENT_SECRET= "FsdfvfvUtHW3-KnumUsfasdfsdcsdfaqqQckAT1U8rK"

#Provide redirect URL 
REDIRECT_URI= "http://127.0.0.1"

#Scopes for get user ID (https://docs.x.com/resources/fundamentals/authentication/guides/v2-authentication-mapping)
SCOPES=tweet.read+users.read

#Provide URL for authorization
AUTH_URI= "https://x.com/i/oauth2/authorize"

#Provide URL for receiving access_token
TOKEN_URI= "https://api.x.com/2/oauth2/token"

*	The task execution requires to authorize in the X in browser, using the URL that script provides. The executor need to press button "Authorize app" and copy redirect URL. The redirect URL should be provided to the script for futher execution. 
*	Example of the authorization URL:

https://x.com/i/oauth2/authorize?response_type=code&client_id=UTsadfas34nV0RFI6MTpjaQ&redirect_uri=http%3A%2F%2F127.0.0.1&scope=tweet.read+users.read&state=1asdf344fgesrtgULHzwKU7Y&code_challenge=kJPYj_Ygk9dfgsdgsert34wbdV7wBW95dz8g&code_challenge_method=S256

*	Example of REDIRECT URL:

http://127.0.0.1/?state=1asdf344fgesrtgULHzwKU7Y&code=bzJsQXA314ygtrgf3869487tygTjghfj544rJHFThjdgfye34RUUT766tgfhjYTZaMWxLOjE3NDE4NjU5NTAxNzk6MToxOmFjOjE

*	During execution in script-directory log-file(main.log) has written.
*	The example of log-file in case of successfull execution:

2025-03-13 14:38:58,617: Let's log!
2025-03-13 14:38:58,619: Have got an authorization URL:
2025-03-13 14:38:58,619: https://x.com/i/oauth2/authorize?response_type=code&client_id=UTsadfas34nV0RFI6MTpjaQ&redirect_uri=http%3A%2F%2F127.0.0.1&scope=tweet.read+tweet.write+users.read+like.write&state=1asdf344fgesrtgULHzwKU7Y&code_challenge=kJPYj_Ygk9dfgsdgsert34wbdV7wBW95dz8g&code_challenge_method=S256
2025-03-13 14:39:18,042: Response status code for access token request is:
2025-03-13 14:39:18,042: 200
2025-03-13 14:39:18,042: Have got an access token.


*	In case of errors during execution of the script, there would be corresponding messages with "ERROR!!!"-lines. The rate-limits error provides additional information in log-file about required pause (in seconds) that have to be done before next try.
* Example of the error-message because of rate-limits exceeded:

2025-03-13 15:23:00,655: ERROR!!! {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
2025-03-13 15:23:00,655: Rate limit exceeded. Retry after 902 seconds.
