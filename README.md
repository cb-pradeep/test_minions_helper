# Minions Helper

General Library for all the Clients and Functions used in all the microservices

## Usage:

To Install:

```pip install git+https://GITHUB_URL```

To Use Microservices:

```
import minion_helpers as minions

# To Invoke Bob Client
bob = minions.summon('bob', endpoint_url="ENDPOINT_URL")
bob.get_all_settings()

```