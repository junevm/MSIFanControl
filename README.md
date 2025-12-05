# MSIFanControl

Fan control TUI for MSI laptops on Linux.
![alt text](assets/image.png)
## Quick Start

### Option A: Install via Go (Recommended)

You can install the tool directly from the repository without cloning:

```sh
# Install 'fan' to your $GOPATH/bin (usually ~/go/bin)
go install gitlab.com/junevm/MSIFanControl/cmd/fan@latest

# Run
$(go env GOPATH)/bin/fan
```

### Option B: Build from Source

```sh
# 1. Clone
git clone https://gitlab.com/junevm/MSIFanControl.git
cd MSIFanControl

# 2. Run directly
task run

# OR Install to /usr/local/bin
task install
```

## Requirements

- Linux (Fedora/RedHat based preferred for auto-setup)
- [Go](https://go.dev/) 1.24+
- [Task](https://taskfile.dev/)

## Supported Models

- MSI GF65 Thin 9SD
  _(May work on others with similar EC layouts)_
