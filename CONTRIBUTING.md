# Contribute to Sublime Text libraries

This document provides some infomation about how to create and register 
libraries for Sublime Text plugin ecosystem.

Libraries must be registered in a repository or channel 
for Package control 4 to deploy them,
very much in the same way as normal pacakges are.


## Deployment sources

Package Control 4 can install libraries from following sources:

1. legacy repository based dependencies,  
   which have been supported since ST3.

   see: https://github.com/packagecontrol/example-dependency

- python wheels shipped via Github/GitLab releases

- python wheels shipped via pypi.org


## Register a library

To register a library globally to Package Control, 
create a [pull request](https://github.com/packagecontrol/channel/pulls) in this Github repository.

Add your library by adding an entry under `"libraries": []`.

The following example illustrates how a registered library looks like,
which is deployed as python wheel via Github releases.

```jsonc
{
	// Help LSP to identify the file as repository.json
	"$schema": "sublime://packagecontrol.io/schemas/repository",

	// Schema 4.0.0+ is required for asset based releases and python 3.8 support
	"schema_version": "4.0.0",

	// The list of registered libraries
	"libraries": [
		{
			"name": "MyLibrary",
			"description": "A custom Sublime Text Library",
			"author": "just me",
			"issues": "https://github.com/packagecontrol/example-dependency/issues",
			"releases": [
				{
					// A glob pattern to extract the relevant download asset from a Github/Gitlab release.
					"asset": "mylibrary--*-py3-none-any.whl",
					// Supported python versions.
					"python_versions": ["3.3", "3.8"]
				}
			]
		}
	]
}
```

For more details about the repository file format,
please refere to [package_control/example-repository.json](https://github.com/wbond/package_control/blob/master/example-repository.json).


## Create a library

### Legacy dependency format

Package Control 4 continues to support the legacy dependency format
as described in https://packagecontrol.io/docs/dependencies.

The format has been extended to support ST4-only and py38-only libraries.

For details, please refer to: https://github.com/packagecontrol/example-dependency

### Python Wheels

To create libraries in python wheel format, 
please follow instructions and tutorials on https://packaging.python.org.

Most important parts are probably how to structure a repository
and how to use `python build` to finally create the wheel files.

Sublime Text specific libraries should be deployed via Githb/GitLab releases.

For instance, use [Github CLI](https://cli.github.com/) command line tool, 
to deploy Sublime Text specific wheel files via Github releases.

#### Example

Perform any required steps to build wheels from source.

```sh
# do any required preparation
# ...

# create wheels
python build ...

# upload wheels as download asset of a Github release
gh release create --target main -t "MyLibrary 1.0.0" "1.0.0" "mylibrary-1.0.0-py3-any-none.whl"
```

Ensure library is registered as asset based release in this repository.
