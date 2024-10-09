# Install

Panoramax CLI can be installed using various methods:

- :simple-python: From [PyPI](https://pypi.org/project/geovisio_cli/), the Python central package repository
- :package: From packaged binaries for Windows & Linux, availaible in the [latest release page](https://gitlab.com/panoramax/clients/cli/-/releases/)
- :simple-git: Using this [Git repository](https://gitlab.com/panoramax/clients/cli)

Panoramax CLI is compatible with all Python versions >= 3.9.

!!! tip

	If your system does not support python 3.9, you can use a tool like [pyenv](https://github.com/pyenv/pyenv) or [uv](https://docs.astral.sh/uv/guides/install-python/#installing-a-specific-version) to install a newer python version.


=== ":fontawesome-brands-windows: Windows"

	On Windows, just download the [latest Windows executable](https://gitlab.com/panoramax/clients/cli/-/releases/) (file named `geovisio_cli-win-amd64.exe`) and open a shell in the download directory (you can do that by typing `cmd` in the explorer opened in the directory).

	Then, simply run:

	```powershell
	geovisio_cli-win-amd64.exe --help
	```

=== ":simple-linux: Linux"

	!!! note
		Linux binary has been built for AMD64. They are built using Ubuntu 22.04, so they should work for all newer versions. For older version though, there might be _libstdc++_ incompatibilities; if you encounter that problem, you can update libstdc++ or install using _PyPi_.

	Download the [latest Linux binary](https://gitlab.com/panoramax/clients/cli/-/releases/) (file named `geovisio_cli-linux-amd64`), then in the download directory:

	```bash
	chmod u+x geovisio_cli-linux-amd64
	./geovisio_cli-linux-amd64 --help
	```

	Optionally, you can put this in /usr/local/bin (if it's in your path) for a simpler use:

	```bash
	chmod u+x geovisio_cli-linux-amd64
	mv geovisio_cli-linux-amd64 /usr/local/bin/geovisio_cli

	geovisio_cli --help
	```

=== ":simple-pypi: PyPI"

	Just run this command:

	```bash
	pip install geovisio_cli
	```

	You should then be able to use the CLI tool with the name `geovisio`:

	```bash
	geovisio --help
	```

	Alternatively, you can use [pipx](https://github.com/pypa/pipx) if you want all the script dependencies to be in a custom virtual env.

	If you choose to [install pipx](https://pypa.github.io/pipx/installation/), then run:

	```bash
	pipx install geovisio_cli
	```

=== ":simple-git: Git"

	Download the repository:

	```bash
	git clone https://gitlab.com/panoramax/clients/cli.git geovisio_cli
	cd geovisio_cli/
	```

	To avoid conflicts, it's considered a good practice to create a _[virtual environment](https://docs.python.org/3/library/venv.html)_ (or virtualenv). To do so, launch the following commands:

	```bash
	# Create the virtual environment in a folder named "env"
	python3 -m venv env

	# Launches utilities to make environment available in your Bash
	source ./env/bin/activate
	```

	Then, install the Panoramax CLI dependencies using pip:

	```bash
	pip install -e .
	```

	You can also install the `dev` and `docs` dependencies if necessary (to have lints, format, tests...):

	```bash
	pip install -e .[dev,docs]
	```

	Then, you can use the `geovisio` command:

	```bash
	geovisio --help
	```
