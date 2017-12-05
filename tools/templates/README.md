# Templates used for SIP code

## `create_sip_package.py`

Simple utility script that creates a new SIP package based on
[Jinja2](http://jinja.pocoo.org/) templates in the `package.j2` directory.
Files with an extension `.j2` are rendered into the specified package path.

Usage:

```bash
  python3 tools/templates/create_sip_package.py [PATH] [TITLE]
```

Where:
-   `[PATH]` is the path of the package to be created, eg.
    `sip/execution_control/master_controller`

-   `[TITLE]` is the
    title given to the package, eg. `Master Controller`.
