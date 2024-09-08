# Package Control Libraries Channel

This repository provides ~~dependency~~ library meta-data for Package Control 4.0.


## Usage

### Receive libraries from this repository

Package Control 4 ships with default configuration to deploy libraries using this channel.

If you encounter any issues with libraries not being available for python 3.8,
make sure to have following lines in _Package Control.sublime-settings_.

```json
"channels": [
	"https://packagecontrol.github.io/channel/channel_v4.json",
	"https://packagecontrol.io/channel_v3.json",
],
```

> [!NOTE]
>
> Keep the order, so items from this channel override those from default channel.


### Using libraries in a Sublime Text package

Tell Package Control, which libraries to install by 
creating a _dependencies.json_ in the root of the package folder,
with all directly or indirectly required libraries (or python packages).

The following example shows a dependencies.json required to use `pydantic` library.
It must also contain all libraries only used by pydantic, such as `pydantic-core` or `typing-extensions`.

```jsonc
{
	// Help LSP to identify the file as dependencies.json
	"$schema": "sublime://packagecontrol.io/schemas/dependencies",

	// operating system: "linux", "osx", "windows", "*"
	"*": {
		// ST build specifier
		">=4107": [
			"annotated-types",
			"eval-type-backport",
			"pydantic",
			"pydantic-core",
			"typing-extensions"
		]
	}
}
```

After saving the file, call `Package Control: Satisfy Libraries` to install them.

see also: [package_control/example-dependencies.md](https://github.com/wbond/package_control/blob/master/example-dependencies.json)

## Contributing

If you want to create or add libraries for Sublime Text, 
please follow [CONTRIBUTING](CONTRIBUTING.md).
