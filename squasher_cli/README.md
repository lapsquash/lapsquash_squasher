oclif-hello-world
=================

oclif example Hello World CLI

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![CircleCI](https://circleci.com/gh/oclif/hello-world/tree/main.svg?style=shield)](https://circleci.com/gh/oclif/hello-world/tree/main)
[![GitHub license](https://img.shields.io/github/license/oclif/hello-world)](https://github.com/oclif/hello-world/blob/main/LICENSE)

<!-- toc -->
* [Usage](#usage)
* [Commands](#commands)
<!-- tocstop -->
# Usage
<!-- usage -->
```sh-session
$ npm install -g @lapsquash/squasher
$ lapsquasher COMMAND
running command...
$ lapsquasher (--version)
@lapsquash/squasher/0.0.1 win32-x64 node-v18.13.0
$ lapsquasher --help [COMMAND]
USAGE
  $ lapsquasher COMMAND
...
```
<!-- usagestop -->
# Commands
<!-- commands -->
* [`lapsquasher help [COMMANDS]`](#lapsquasher-help-commands)
* [`lapsquasher plugins`](#lapsquasher-plugins)
* [`lapsquasher plugins:install PLUGIN...`](#lapsquasher-pluginsinstall-plugin)
* [`lapsquasher plugins:inspect PLUGIN...`](#lapsquasher-pluginsinspect-plugin)
* [`lapsquasher plugins:install PLUGIN...`](#lapsquasher-pluginsinstall-plugin-1)
* [`lapsquasher plugins:link PLUGIN`](#lapsquasher-pluginslink-plugin)
* [`lapsquasher plugins:uninstall PLUGIN...`](#lapsquasher-pluginsuninstall-plugin)
* [`lapsquasher plugins:uninstall PLUGIN...`](#lapsquasher-pluginsuninstall-plugin-1)
* [`lapsquasher plugins:uninstall PLUGIN...`](#lapsquasher-pluginsuninstall-plugin-2)
* [`lapsquasher plugins update`](#lapsquasher-plugins-update)

## `lapsquasher help [COMMANDS]`

Display help for lapsquasher.

```
USAGE
  $ lapsquasher help [COMMANDS] [-n]

ARGUMENTS
  COMMANDS  Command to show help for.

FLAGS
  -n, --nested-commands  Include all nested commands in the output.

DESCRIPTION
  Display help for lapsquasher.
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v5.2.9/src/commands/help.ts)_

## `lapsquasher plugins`

List installed plugins.

```
USAGE
  $ lapsquasher plugins [--core]

FLAGS
  --core  Show core plugins.

DESCRIPTION
  List installed plugins.

EXAMPLES
  $ lapsquasher plugins
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v2.4.7/src/commands/plugins/index.ts)_

## `lapsquasher plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ lapsquasher plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.
  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.


ALIASES
  $ lapsquasher plugins add

EXAMPLES
  $ lapsquasher plugins:install myplugin 

  $ lapsquasher plugins:install https://github.com/someuser/someplugin

  $ lapsquasher plugins:install someuser/someplugin
```

## `lapsquasher plugins:inspect PLUGIN...`

Displays installation properties of a plugin.

```
USAGE
  $ lapsquasher plugins:inspect PLUGIN...

ARGUMENTS
  PLUGIN  [default: .] Plugin to inspect.

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

GLOBAL FLAGS
  --json  Format output as json.

DESCRIPTION
  Displays installation properties of a plugin.

EXAMPLES
  $ lapsquasher plugins:inspect myplugin
```

## `lapsquasher plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ lapsquasher plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.
  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.


ALIASES
  $ lapsquasher plugins add

EXAMPLES
  $ lapsquasher plugins:install myplugin 

  $ lapsquasher plugins:install https://github.com/someuser/someplugin

  $ lapsquasher plugins:install someuser/someplugin
```

## `lapsquasher plugins:link PLUGIN`

Links a plugin into the CLI for development.

```
USAGE
  $ lapsquasher plugins:link PLUGIN

ARGUMENTS
  PATH  [default: .] path to plugin

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Links a plugin into the CLI for development.
  Installation of a linked plugin will override a user-installed or core plugin.

  e.g. If you have a user-installed or core plugin that has a 'hello' command, installing a linked plugin with a 'hello'
  command will override the user-installed or core plugin implementation. This is useful for development work.


EXAMPLES
  $ lapsquasher plugins:link myplugin
```

## `lapsquasher plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ lapsquasher plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ lapsquasher plugins unlink
  $ lapsquasher plugins remove
```

## `lapsquasher plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ lapsquasher plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ lapsquasher plugins unlink
  $ lapsquasher plugins remove
```

## `lapsquasher plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ lapsquasher plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ lapsquasher plugins unlink
  $ lapsquasher plugins remove
```

## `lapsquasher plugins update`

Update installed plugins.

```
USAGE
  $ lapsquasher plugins update [-h] [-v]

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Update installed plugins.
```
<!-- commandsstop -->
