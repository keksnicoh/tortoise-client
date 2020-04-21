# tortoise-client

this repository contains several scripts which are executed on a raspberry pi sending data to [tortoise-service][1].

## example profile

```bash
TURTLE_HOST=http://192.168.178.21:8081/
TURTLE_STATUS_API="${TURTLE_HOST}v1/status"
```

## example commands

```bash
source ~/tortoise-client/.profile; python3 bin/send_status.py --api=$TURTLE_STATUS_API
```

[1]: https://github.com/keksnicoh/turtle-service/
