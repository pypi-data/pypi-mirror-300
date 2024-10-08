# sopel-http-codes

Sopel plugin to look up standard HTTP status codes.


## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:
 
```shell
$ pip install sopel-http-codes
```

### Requirements

This plugin is written for:

* Python 3.8+
* Sopel 8.0+


## Using

Commands & arguments:

`.http <code>`: Returns the name of the given status `<code>` and a brief
description of its purpose from Python's `http` module, along with a link to an
image macro showing a cat or dog personifying(?) that status code.
