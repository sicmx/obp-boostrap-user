# Auto create initial Open Bank Project user

Useful for automating deployment of open bank project; can
be used to bootstrap an initial user in a controlled way.

- Uses python 3
- Boostrap an Open Bank Project user automatically

## Requirements

```
pip install -r requirements.txt
```

## Run

- First, edit `.env` with desired account info (double check password policy, else with fail on insecure / invalid password)

```
source .env # otherwise with read from environmet (e.g Kubernetes controlled)
python create_new_user.py # Register new user
```

Note: Setting `MOZ_HEADLESS=1` takes firefox into headless mode (see `.env`)
