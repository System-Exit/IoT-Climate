# Programming Internet of Things

## Branches

- **master:** Mostly Documentation
- **ass1:** Assignment 1 master branch
- **ass1-dev:** Assignment 1 development branch

## Contributors

- [Contributors](https://github.com/Volkor3-16/piot/graphs/contributors)

## License

- see [LICENSE](https://github.com/Volkor3-16/piot/blob/master/LICENSE.md) file

## Installation of Weather Services

1. Clone or download this branch. `git clone -b branchname`
2. Copy the systemd services. `sudo mv weathermonitor.service /etc/systemd/system/ && sudo mv weatherbluetooth.service /etc/systemd/system/`
3. Set Owner correctly. `sudo chown root:root /etc/systemd/system/weathermonitor.service && sudo chown root:root /etc/systemd/system/weatherbluetooth.service`
4. Set Permissions correctly `sudo chmod 644 /etc/systemd/system/weathermonitor.service && sudo chmod 644 /etc/systemd/system/weatherbluetooth.service`
5. reload, and start services `sudo systemctl daemon-reload && sudo systemctl start weathermonitor weatherbluetooth`