from setuptools import setup

name = "types-six"
description = "Typing stubs for six"
long_description = '''
## Typing stubs for six

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`six`](https://github.com/benjaminp/six) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`six`.

This version of `types-six` aims to provide accurate annotations
for `six==1.16.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/six. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`4b11151a0c70a09049c69d8fe69351a739472fea`](https://github.com/python/typeshed/commit/4b11151a0c70a09049c69d8fe69351a739472fea) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="1.16.21.20241009",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/six.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['six-stubs'],
      package_data={'six-stubs': ['__init__.pyi', 'moves/BaseHTTPServer.pyi', 'moves/CGIHTTPServer.pyi', 'moves/SimpleHTTPServer.pyi', 'moves/__init__.pyi', 'moves/_dummy_thread.pyi', 'moves/_thread.pyi', 'moves/builtins.pyi', 'moves/cPickle.pyi', 'moves/collections_abc.pyi', 'moves/configparser.pyi', 'moves/copyreg.pyi', 'moves/email_mime_base.pyi', 'moves/email_mime_multipart.pyi', 'moves/email_mime_nonmultipart.pyi', 'moves/email_mime_text.pyi', 'moves/html_entities.pyi', 'moves/html_parser.pyi', 'moves/http_client.pyi', 'moves/http_cookiejar.pyi', 'moves/http_cookies.pyi', 'moves/queue.pyi', 'moves/reprlib.pyi', 'moves/socketserver.pyi', 'moves/tkinter.pyi', 'moves/tkinter_commondialog.pyi', 'moves/tkinter_constants.pyi', 'moves/tkinter_dialog.pyi', 'moves/tkinter_filedialog.pyi', 'moves/tkinter_tkfiledialog.pyi', 'moves/tkinter_ttk.pyi', 'moves/urllib/__init__.pyi', 'moves/urllib/error.pyi', 'moves/urllib/parse.pyi', 'moves/urllib/request.pyi', 'moves/urllib/response.pyi', 'moves/urllib/robotparser.pyi', 'moves/urllib_error.pyi', 'moves/urllib_parse.pyi', 'moves/urllib_request.pyi', 'moves/urllib_response.pyi', 'moves/urllib_robotparser.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
