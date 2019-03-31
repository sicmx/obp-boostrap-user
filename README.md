# Bootstrap an Open Bank Project kubernetes cluster

Useful for automating deployment of open bank project; can
be used to bootstrap an initial user in a controlled way.

- Uses python 3
- Boostrap an Open Bank Project user automatically

## Requirements

```
pip install -r requirements.txt
```

## Run / How to bootstrap an Open Bank Project Deployment


Start deploy Open Bank Project on Kubernetes cluster:

```
kubectl apply -f obpapi_k8s.yaml 
```
Watch / wait for pod creation to complete:
```
kubectl get -w pods
NAME                              READY   STATUS              RESTARTS   AGE
obp-deployment-77955dd88f-zfrf4   0/1     ContainerCreating   0          7s
postgres-5cdc48899c-49l22         0/1     ContainerCreating   0          7s
### Eventually...
obp-deployment-77955dd88f-zfrf4   1/1     Running             0          68s
postgres-5cdc48899c-49l22         1/1     Running             0          80s
```

(optional) Verify / View the service is active:
```
minikube service opbapi-service #Two will open, only the web service will load
``

Finally, bootstrap the user:

- First, edit `.env` with desired account info (double check password policy, else with fail on insecure / invalid password) 
- For example, if testing locally, change OBP_HOST in `.env` to the hostname and port minikube gave you.

```
# Edit .env with your desired credentials then:
source .env # otherwise with read from environmet (e.g Kubernetes controlled)
python3 bootstrap.py # Registers new user, a new consumer, and gets user id
# No news is good news. If completes without error, you'll see nothing.
```

## Patch the deployment with super user
```
# Create patch-deployment.yaml for obpapi deployment
sed s/REPLACE_ME/`cat obp_user_id.txt`/g patch-deployment.yaml.example > patch-deployment.yaml;
# Update the deployment
kubectl patch deployment obp-deployment --patch "$(cat patch-deployment.yaml)"
# (optional) watch your new deployment roll out:
kubectl get -w pods # Kubetnetes will kill existing pods, deploying new ones with this new config merged
```

Note: Setting `MOZ_HEADLESS=1` takes firefox into headless mode (see `.env`)

