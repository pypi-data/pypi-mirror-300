## test

```shell
(venv) ➜  libtoolbox poetry run pytest 
Configuration file exists at /Users/huoyinghui/Library/Application Support/pypoetry, reusing this directory.

Consider moving configuration to /Users/huoyinghui/Library/Preferences/pypoetry, as support for the legacy directory will be removed in an upcoming release.
========================================================================= test session starts ==========================================================================
platform darwin -- Python 3.10.1, pytest-8.3.2, pluggy-1.5.0
rootdir: /Users/huoyinghui/github/pytools/libtoolbox
configfile: pyproject.toml
plugins: anyio-3.6.2
collected 1 item                                                                                                                                                       

tests/test_path.py .                                                                                                                                             [100%]

========================================================================== 1 passed in 0.02s ===========================================================================
(venv) ➜  libtoolbox
```


## build

```shell
(venv) ➜  pytools cd libtoolbox 
(venv) ➜  libtoolbox  poetry build
Configuration file exists at /Users/huoyinghui/Library/Application Support/pypoetry, reusing this directory.

Consider moving configuration to /Users/huoyinghui/Library/Preferences/pypoetry, as support for the legacy directory will be removed in an upcoming release.
Building libtoolbox (0.1.0)
  - Building sdist
  - Built libtoolbox-0.1.0.tar.gz
  - Building wheel
  - Built libtoolbox-0.1.0-py3-none-any.whl
(venv) ➜  libtoolbox 
```

## publish

``` shell
venv) ➜  libtoolbox twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Uploading libtoolbox-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.0/5.0 kB • 00:00 • ?
Uploading libtoolbox-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 kB • 00:00 • ?

View at:
https://pypi.org/project/libtoolbox/0.1.0/
(venv) ➜  libtoolbox 
```

## install
```
(venv) ➜  libtoolbox pip install -i https://pypi.org/simple  libtoolbox
Collecting libtoolbox
  Downloading libtoolbox-0.1.0-py3-none-any.whl (1.6 kB)
Installing collected packages: libtoolbox
Successfully installed libtoolbox-0.1.0

[notice] A new release of pip available: 22.3.1 -> 24.2
[notice] To update, run: pip install --upgrade pip
(venv) ➜  libtoolbox 
```