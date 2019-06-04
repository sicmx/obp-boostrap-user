import os
from create_new_user import create_new_user
from create_consumer import create_consumer
from obp_python import getAuthToken, getUserId
import json

# Register new user
create_new_user()

# Create consumer (to generate consumer key & secret)
create_consumer()

# Get auth token
req = getAuthToken(OBP_CONSUMER_KEY=os.environ['OBP_CONSUMER_KEY'], OBP_API_HOST=os.environ['OBP_API_HOST'], OBP_USERNAME=os.environ['OBP_USERNAME'], OBP_PASSWORD=os.environ['OBP_PASSWORD'])

auth_token = json.loads(req.text)['token']

os.environ['OBP_AUTH_TOKEN'] = auth_token

# Get user id
req = getUserId()
userId = json.loads(req.text)['user_id']
# Write user id to file
with open('obp_user_id.txt', 'w') as fp:
  fp.write(userId)


# Inject super user id into kubernetest secret

# Delete obpapi-service, redeploy new secret config map with superuser id 
