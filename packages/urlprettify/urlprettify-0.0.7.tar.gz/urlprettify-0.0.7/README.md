# Prettify URL to use only FQDN or IP-address

## How to use

```python
from urlprettify import urlprettify

ugly_url = "hxxxps[:]//test[.]io/spam.php"
pretty_url = urlprettify.prettify(ugly_url)
```

## Options for conversion

- Conversion.NO_PREFIX - Remove scheme prefix
- Conversion.NO_SUFFIX - Remove trailing suffix (port, path)
- Conversion.NO_BRACES - Remove braces

```python
from urlprettify import urlprettify

ugly_url = "hxxxps[:]//test[.]io/spam.php"
pretty_url = urlprettify.prettify(ugly_url, urlprettify.Conversion.NO_PREFIX | urlprettify.Conversion.NO_SUFFIX)
```
