# Bootstrap an Open Bank Project kubernetes cluster

## Goals

- Start with an empty kubernetes cluster
- Leave with a deployed Open Bank Project sandbox
- With one super user bootstrapped automatically activated (config defined credentials)
- Objective: Ready to work on developing core bank adapters quickly and easily

This is useful for automating deployment of open bank project; can
be used to bootstrap an initial user in a controlled way.

## Run / How to bootstrap an Open Bank Project Deployment


Start deploy Open Bank Project on Kubernetes cluster:

```
git clone https://github.com/chrisjsimpson/obp-boostrap-user.git;
cd obp-boostrap-user;
kubectl apply -f https://raw.githubusercontent.com/chrisjsimpson/obp-kubernetes/master/obpapi_k8s.yaml
```
What the above does is tell kubernetes to fetch obpapi_k8s.yaml, read its contents, and deploy the following services:

  - Open Bank Project deployment (jetty instance(s), contains the bulk of Open Bank Project)
  - Postgres deployment (needed for stateful storage)

Watch / wait for pod creation to complete:
```
kubectl get -w pods
NAME                              READY   STATUS              RESTARTS   AGE
obp-deployment-77955dd88f-zfrf4   0/1     ContainerCreating   0          7s
postgres-5cdc48899c-49l22         0/1     ContainerCreating   0          7s
### Eventually... after a short while, all will be in 'Running' state
obp-deployment-77955dd88f-zfrf4   1/1     Running             0          68s
postgres-5cdc48899c-49l22         1/1     Running             0          80s
```

Verify / View the service is active:
```
# If you're running locally on minikube
minikube service opbapi-service #Two will open, only the web service will load
# Or, if you're running Cloud hosted kubernetes (AWS, Google, IBM, Digital Ocean etc):
kubectl get services # look for the 'External-IP' address if you want to visit on your browser
```
**Note:** You cannot bootstrap (automatic user creation, consumer and superuser) until 
Open Bank Project is fully loaded. 

Finally, bootstrap the user:

Get boostrap.yaml, and edit the `env` to your liking (user name, password):

```
wget https://raw.githubusercontent.com/chrisjsimpson/obp-kubernetes/master/bootstrap.yaml
```

Add the bootstrap tool to your Open Bank Project cluster:
```
kubectl apply -f bootstrap.yaml
kubectl get -w pods # Wait until bootstap is 'running'
kubectl exec bootstrap python3 bootstrap.py # Wait for it to complete
kubectl cp default/bootstrap:obp_user_id.txt ./ # get user id
```
### Create patch-deployment.yaml for obpapi deployment
```
## Patch the deployment with super user
sed s/REPLACE_ME/`cat obp_user_id.txt`/g patch-deployment.yaml.example > patch-deployment.yaml;
# Update the deployment
kubectl patch deployment obp-deployment --patch "$(cat patch-deployment.yaml)"
# (optional) watch your new deployment roll out:
kubectl get -w pods # Kubetnetes will kill existing pods, deploying new ones with this new config merged
```

You're done!

#### Locally / if not using kubernetes
- First, edit `.env` with desired account info (double check password policy, else with fail on insecure / invalid password) 
- For example, if testing locally, change OBP_HOST in `.env` to the hostname and port minikube gave you.
- Note: Setting `MOZ_HEADLESS=1` takes firefox into headless mode (see `.env`)

```
pip install -r requirements.txt
```
```
# Edit .env with your desired credentials then:
source .env # otherwise with read from environmet (e.g Kubernetes controlled)
python3 bootstrap.py # Registers new user, a new consumer, and gets user id
# No news is good news. If completes without error, you'll see nothing.
```

##### More info 

To understand updating deployments see: https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/
