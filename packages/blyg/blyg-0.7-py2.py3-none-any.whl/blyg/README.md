# Blyg (shy)

Is a sharing platform that utilizes websockets and end-to-end encryption.
There's browser support through javascript, as well as a cli tool
that allows Linux users to upload from the terminal.

## Examples


### Starting a receiver

```
$ blyg receive --path ~/Downloads
```

This will give you a session ID that you can share to others.
Once someone sends you a file - it will ask you for approval to receive.
And if accepted, it will end up in `Downloads`.

### Starting an upload

```
$ blyg upload --path ./test.txt --id 7456
```

`7456` is the session ID of the `receive` command.