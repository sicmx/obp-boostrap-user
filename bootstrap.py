import os
from create_new_user import create_new_user
from create_consumer import create_consumer
from obp_python import getAuthToken, getUserId

# Register new user
create_new_user()

# Create consumer (to generate consumer key & secret)
create_consumer()

# Get auth token
auth_token = getAuthToken(CONSUMER_KEY=os.environ['CONSUMER_KEY'], OBP_API_HOST=os.environ['OBP_API_HOST'], OBP_USERNAME=os.environ['OBP_USERNAME'], PASSWORD=os.environ['OBP_PASSWORD'])

# Get user id
userId = getUserId(OBP_AUTH_TOKEN=auth_token,OBP_API_HOST=os.environ['OBP_API_HOST'])

# Write user id to file
with open('obp_user_id.txt', 'w') as fp:
  fp.write(userId)


# Inject super user id into kubernetest secret

# Delete obpapi-service, redeploy new secret config map with superuser id 
