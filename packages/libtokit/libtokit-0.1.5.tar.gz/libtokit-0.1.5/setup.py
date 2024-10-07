# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libtokit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libtokit',
    'version': '0.1.5',
    'description': 'A simple utility for creating directories.',
    'long_description': '## test\n\n```shell\n(venv) ➜  libtoolbox poetry run pytest \nConfiguration file exists at /Users/huoyinghui/Library/Application Support/pypoetry, reusing this directory.\n\nConsider moving configuration to /Users/huoyinghui/Library/Preferences/pypoetry, as support for the legacy directory will be removed in an upcoming release.\n========================================================================= test session starts ==========================================================================\nplatform darwin -- Python 3.10.1, pytest-8.3.2, pluggy-1.5.0\nrootdir: /Users/huoyinghui/github/pytools/libtoolbox\nconfigfile: pyproject.toml\nplugins: anyio-3.6.2\ncollected 1 item                                                                                                                                                       \n\ntests/test_path.py .                                                                                                                                             [100%]\n\n========================================================================== 1 passed in 0.02s ===========================================================================\n(venv) ➜  libtoolbox\n```\n\n\n## build\n\n```shell\n(venv) ➜  pytools cd libtoolbox \n(venv) ➜  libtoolbox  poetry build\nConfiguration file exists at /Users/huoyinghui/Library/Application Support/pypoetry, reusing this directory.\n\nConsider moving configuration to /Users/huoyinghui/Library/Preferences/pypoetry, as support for the legacy directory will be removed in an upcoming release.\nBuilding libtoolbox (0.1.0)\n  - Building sdist\n  - Built libtoolbox-0.1.0.tar.gz\n  - Building wheel\n  - Built libtoolbox-0.1.0-py3-none-any.whl\n(venv) ➜  libtoolbox \n```\n\n## publish\n\n``` shell\nvenv) ➜  libtoolbox twine upload dist/*\nUploading distributions to https://upload.pypi.org/legacy/\nUploading libtoolbox-0.1.0-py3-none-any.whl\n100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.0/5.0 kB • 00:00 • ?\nUploading libtoolbox-0.1.0.tar.gz\n100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 kB • 00:00 • ?\n\nView at:\nhttps://pypi.org/project/libtoolbox/0.1.0/\n(venv) ➜  libtoolbox \n```\n\n## install\n```\n(venv) ➜  libtoolbox pip install -i https://pypi.org/simple  libtoolbox\nCollecting libtoolbox\n  Downloading libtoolbox-0.1.0-py3-none-any.whl (1.6 kB)\nInstalling collected packages: libtoolbox\nSuccessfully installed libtoolbox-0.1.0\n\n[notice] A new release of pip available: 22.3.1 -> 24.2\n[notice] To update, run: pip install --upgrade pip\n(venv) ➜  libtoolbox \n```',
    'author': 'pytools',
    'author_email': 'hyhlinux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
