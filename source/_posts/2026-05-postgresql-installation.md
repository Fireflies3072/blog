---
title: PostgreSQL Installation and Configuration Guide
date: 2026-05-15 21:44:57
tags: [database]
categories: [Articles]
cover: https://cdn.fireflies3072.com/blog/2026-05-postgresql-installation/cover.png
excerpt: PostgreSQL is a powerful, open-source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. This guide will walk you through the installation on Ubuntu, basic configuration, and setting up a management tool.
---

## Introduction

PostgreSQL is a powerful, open-source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. This guide will walk you through the installation on Ubuntu, basic configuration, and setting up a management tool.

## Installation on Ubuntu

For the latest version of PostgreSQL, it is recommended to use the official PostgreSQL Apt Repository.

Follow the guide on [PostgreSQL Ubuntu Download page](https://www.postgresql.org/download/linux/ubuntu/) for specific instructions.

### Checking PostgreSQL Status

After installation, you can verify that the PostgreSQL service is running using `systemctl`:

```bash
sudo systemctl status postgresql
```

You can also start, stop, or restart the service with the following commands:

```bash
sudo systemctl start postgresql
sudo systemctl stop postgresql
sudo systemctl restart postgresql
```

## Setting the postgres User Password

By default, PostgreSQL has `postgres` user which has no password. For local access, a password is not needed. However, for remote access purpose, we have to setup a strong password.

1. Access the PostgreSQL prompt:
   ```bash
   sudo -u postgres psql
   ```
   Now the command line will become `postgres=#`

2. Set the password using the `ALTER USER` command:
   ```sql
   ALTER USER postgres WITH PASSWORD 'STRONG_PASSWORD';
   ```

3. Exit the prompt:
   ```sql
   \q
   ```

## Setting up SSL Certificates

The password is just for authentication purpose. Without certificate, the transmission content is not encrypted. Therefore, we have to setup a certificate for PostgreSQL.

### Existing Certificate

1. Put certificate files in data directory.

```bash
cd /var/lib/postgresql/18/main
```

2. Modify permission

```bash
# Modify owner and group
sudo chown postgres:postgres server.key server.pem

# Set private key permission (editable by owner)
sudo chmod 600 server.key

# Set certificate permission (read-only)
sudo chmod 644 server.pem
```

3. Modify configuration file

```bash
cd ..
sudo vim postgresql.conf
```

```toml
ssl = on
ssl_cert_file = 'server.pem'
ssl_key_file = 'server.key'
```

4. Restart PostgreSQL to apply the changes:

```bash
sudo systemctl restart postgresql
```

### Create a Self-Signed Certificate

For testing purposes, you can generate a self-signed certificate:

```bash
openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
chmod 0600 server.key
```

## Installing Database Manager

DBeaver is a free multi-platform database tool for developers, database administrators, and analysts.

Download at [https://dbeaver.io/download/](https://dbeaver.io/download/)
