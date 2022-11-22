```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```toml
[project]
name = "example_package_YOUR_USERNAME_HERE"
version = "0.0.1"
authors = [
  { name="Example Author", email="author@example.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"
```

```bash
python3 -m pip install --upgrade build
```

```bash
python3 -m build
```

```bash
python3 -m pip install --upgrade twine
```

```bash
python3 -m twine upload --repository pypi dist/*
```


