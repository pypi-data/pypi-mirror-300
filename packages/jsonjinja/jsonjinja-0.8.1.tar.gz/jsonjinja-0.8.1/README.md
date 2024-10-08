# jsonjinja

Jinja2 Templating with JSON files

## Example

`example.txt.jinja`:

```
{{ text }}

```

`example.json`:

```json
{
    "text": "Hello, world."
}
```

You run:

```console
$ jsonjinja -o result.txt example.txt.jinja example.json
```

Then you get `result.txt`:

```
Hello, world.

```

## Install

```console
$ pip install jsonjinja
```


## Usage


```
usage: jsonjinja [-h] [-i IMPORT_NAME] [-o OUTPUT] template_file [json_files ...]

positional arguments:
  template_file         Jinja2 template file
  json_files            JSON files loaded to the context (top-level object must be a dictionary)

optional arguments:
  -h, --help            show this help message and exit
  -i IMPORT_NAME, --import IMPORT_NAME
                        import Python module to the context (can be put multiple times)
  -o OUTPUT, --output OUTPUT
                        output file name
```

Installed `jsonjinja` command runs `main` function of `jsonjinja.py`, which is
the sole entire content of the module.

You can copy `jsonjinja.py` and add it to your project freely.  See the License
section bellow.

## References

- [Template Designer Documentation — Jinja Documentation (3.1.x)][1]
- [JSON][2]

[1]:https://jinja.palletsprojects.com/en/3.1.x/templates/
[2]:https://www.json.org/

## License

jsonjinja is marked with CC0 1.0. To view a copy of
this license, visit &lt;https://creativecommons.org/publicdomain/zero/1.0/&gt;.

(In other words, public domain.)
