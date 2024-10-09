# Access Tokens

The `snip.token` module provides functionalities to manage tokens, which are used for authentication with a snip instance. Tokens can be stored in various sources, including keyring and files.


## Token Class

The `Token` class represents a token object and holds information such as the token name, book ID, token string, and deployment URL.



## Storage

We provide two storage modules to store and retrieve tokens: [`file_store`](#token/file_store) and [`keyring_store`](#token/keyring_store). Both modules provide functionalities to store, retrieve, and remove tokens.


To get all available tokens you may use the `get_all_tokens` function. This function will return a list of all available tokens.



(token/file_store)=
### File Storage




(token/keyring_store)=
### Keyring Storage

