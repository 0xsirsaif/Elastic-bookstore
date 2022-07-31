#### Use ``HTTPie`` as a client

##### Endpoints

1. ``GET`` specific Book with ``ID``.

```shell
http --json GET :8000/bookstore/[ID]
```

2. ``GET`` all Books.

```shell
http --json GET :8000/bookstore/
```

3. ``PUT`` or modify Book, validated with Pydantic ``Book`` model.

```shell
http --json PUT :8000/bookstore/[ID] [KEY/Value]
```
