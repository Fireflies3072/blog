---
title: Getting Started with FRP: A Comprehensive Setup Guide
date: 2026-05-15 19:48:15
tags:
---

## Introduction

FRP (Fast Reverse Proxy) is a high-performance reverse proxy application that allows you to expose a local server behind a NAT or firewall to the internet. It is particularly useful for scenarios where you need to access services on your home or office network from anywhere in the world.

### Why use FRP?

- **Easy to use**: Simple configuration files and straightforward deployment.
- **Versatile**: Supports multiple protocols including TCP, UDP, HTTP, and HTTPS.
- **High Performance**: Optimized for speed and low resource usage.
- **Security**: Supports encryption and compression for data transmission.

## Download FRP

You can find the latest releases of frp on their official GitHub repository: [https://github.com/fatedier/frp](https://github.com/fatedier/frp).

### Steps to download:

1. Go to the [Releases](https://github.com/fatedier/frp/releases) page.
2. Select the version appropriate for your operating system (e.g., [frp_0.68.1_linux_amd64.tar.gz](https://github.com/fatedier/frp/releases/download/v0.68.1/frp_0.68.1_linux_amd64.tar.gz)).

### Linux Command:

To download and extract frp on a Linux server, you can use the following commands:

```bash
wget https://github.com/fatedier/frp/releases/download/v0.68.1/frp_0.68.1_linux_amd64.tar.gz
tar -zxvf frp_0.68.1_linux_amd64.tar.gz
cd frp_0.68.1_linux_amd64
```

Remember to replace the link and filename with the one you want.

## Configure FRPS

`frps` is the server-side component that should be run on a machine with a public IP address.

1. Locate the `frps.toml` file in the extracted directory.
2. Edit the configuration to specify the port frps will listen on:

```toml
# 1. frp listening setting
bindPort = 7000

# 2. Authentication setting
auth.method = "token"
auth.token = "REPLACE WITH YOUR STRONG PASSWORD"

# 3. Web dashboard (Check status)
webServer.addr = "0.0.0.0"
webServer.port = 7500        # Access IP:7500 by browser
webServer.user = "DASHBOARD USERNAME"
webServer.password = "DASHBOARD PASSWORD"

# 4. Port white list
allowPorts = [
  { start = 5432, end = 5432 }
]
```

3. Start the server:

```bash
./frps -c ./frps.toml
```

## Configure FRPC

`frpc` is the client-side component that runs on your local machine behind the NAT.

1. Locate the `frpc.toml` file.
2. Configure it to connect to your `frps` server and define the services you want to expose:

```toml
# 1. Connection with server
serverAddr = "x.x.x.x"       # Your server public IP
serverPort = 7000            # Must be the same as bindPort in frps.toml

# 2. Authetication setting
auth.method = "token"
auth.token = "REPLACE WITH YOUR STRONG PASSWORD" # Must be the same as auth.token in frps.toml

# 3. Enable TLS
transport.tls.enable = true

# 4. Proxy setting
[[proxies]]
name = "proxy-service"
type = "tcp"                 # Protocol
localIP = "127.0.0.1"
localPort = 5432
remotePort = 5432
```

3. Start the client:

```bash
./frpc -c ./frpc.toml
```

## Configure systemd

To allow frps and frpc to run stably in the background and start on boot, we will configure systemd.

1. Move the executable file to system directory.

frps:

```bash
sudo cp frps /usr/local/bin/
```

frpc:

```bash
sudo cp frpc /usr/local/bin/
```

2. Create systemd config directory.

frps:

```bash
sudo mkdir /etc/frp && sudo cp frps.toml /etc/frp/
```

frpc:

```bash
sudo mkdir /etc/frp && sudo cp frpc.toml /etc/frp/
```

3. Create service file.

frps:

```bash
sudo vim /etc/systemd/system/frps.service
```

```toml
[Unit]
Description=Frp Server Service
After=network.target

[Service]
Type=simple
User=nobody
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/frps -c /etc/frp/frps.toml

[Install]
WantedBy=multi-user.target
```

frpc:

```bash
sudo vim /etc/systemd/system/frpc.service
```

```toml
[Unit]
Description=Frp Client Service
After=network.target

[Service]
Type=simple
User=nobody
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/frpc -c /etc/frp/frpc.toml

[Install]
WantedBy=multi-user.target
```

4. Start service.

frps:

```bash
sudo systemctl enable frps
sudo systemctl start frps
```

frpc:

```bash
sudo systemctl enable frpc
sudo systemctl start frpc
```
