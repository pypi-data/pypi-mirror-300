# bapp-store

This is a simple app store for Beepy applications.

It works by querying Github for repos with the topic `beepy-app`, cloning them,
installing them through a `justfile`, and providing some basic interfacing such
as searching, installing, listing, and deleting applications.


## Installation

You can install the `bapp-store` by simply running `pipx install bapp-store`.


## Usage

`bapp-store` - Brings up the TUI
`bapp-store --list` - List applications found on Github
`bapp-store --search <name>` - Searches for a Beepy app on Github
`bapp-store --install <name>` - Install a Beepy app from Github
`bapp-store --installed` - List installed applications
`bapp-store --remove <name>` - Removes the Beepy app from your device


## Future Work

There should be some concept of app versioning and pinning/installing particular
versions.
