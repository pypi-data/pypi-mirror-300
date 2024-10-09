# bwfilters

Simple whitelist/blacklist filter structures.


```python
from bwfilters import BWFilter

data = ['good', 'nice', 'bad']

my_filter = BWFilter()
my_filter.whitelist = ['good', 'nice']

my_filter.filter(lambda x: x, data)
>>> ['good', 'nice']
```


## Installation

```bash
pip install bwfilters
```



## License

[![License: GPL  v2.1][license-shield]][gnu]

This software is distributed under the [General Public License v2][license],
more information available at the [Free Software Foundation][gnu].


<!-- LICENSE -->

[license]: LICENSE "General Public License v2"
[gnu]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "Free Software Foundation"
[license-shield]: https://img.shields.io/github/license/sanjacob/bwfilters


<!-- SHIELD LINKS -->

[pypi]: https://pypi.org/project/bwfilters


<!-- SHIELDS -->

[pypi-shield]: https://img.shields.io/pypi/v/bwfilters
[build-shield]: https://img.shields.io/github/actions/workflow/status/sanjacob/bwfilters/build.yml?branch=master
[docs-shield]: https://img.shields.io/readthedocs/bwfilters
