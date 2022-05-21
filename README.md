# Onceler

"*How ba-a-a-ad can I be?*"

Cutting down the Lorax since 2021.

Onceler is a wrapper for Lorax that allows for advanced image composition.

Onceler uses a config file called `onceler.toml` to define the image compose.

The config file is a TOML that contains the project data, and various data for each variants

A variant is a section that starts with `variant-*` and contains the type and data necessary to initiate the compose.

Example of a onceler config:
```toml
#onceler.toml
[image]
releasever = 36

[variant-workstation]
kickstart = "fedora-workstation-live.ks"
type = "iso"


[variant-docker]
kickstart = "fedora-docker.ks"
type = "iso"

```


## Why?
Becuase long command line arguments are always a pain. Why not turn them into a config file?