---
title: Set Up a Simple File Server on Linux with Nginx
date: 2025-05-24 14:31:09
tags: [linux, server]
categories: [Articles]
cover: https://cdn.fireflies3072.com/blog/2025-05-file-server/cover.jpg
excerpt: When you need a quick, high-performance, read-only file server on a Linux machine, Nginx is often the best solution. It's stable, fast, and remarkably simple to configure for serving static content and directory listings.
---

## Setup and Configuration



### Install Nginx

Ensure the Nginx web server package is installed on your Linux distribution.

**Debian/Ubuntu-based systems**

```bash
sudo apt update
sudo apt install nginx
```

**RHEL/CentOS/Fedora-based systems**

Early systems

```bash
sudo yum install nginx
```

Latest systems

```bash
sudo dnf install nginx
```



### Create the Shared Directory

Define the directory you intend to share via Nginx. Using a path outside of the default web root (`/var/www/html`) is often cleaner.

This is an example to create a folder at `/srv/file_share`.

```
sudo mkdir -p /srv/file_share
```



### Configure Nginx

We will create a specific configuration file in the `/etc/nginx/conf.d/` directory. This is often the simplest method, as modern Nginx installations are pre-configured to automatically include files from this location.

Create the file and name it appropriately (e.g., `file_server.conf`):

```bash
sudo vim /etc/nginx/conf.d/file_server.conf
```

Paste the following `server` block configuration. We will use port `10000` to avoid conflicts. **Remember to replace `your_server_ip_or_domain` with your own setting.**

```nginx
server {
    listen 10000; # Listen on the custom port
    server_name your_server_ip_or_domain;

    location / {
        # Set the root directory for the files
        root /srv/file_server; 

        # 1. ESSENTIAL: Enables directory browsing (file listings)
        autoindex on; 

        # 2. Optional: Show sizes in KB, MB, GB format
        autoindex_exact_size off; 
        
        # 3. Optional: Sort listing by modification time
        autoindex_localtime on; 

        # 4. Optional: If no index.html is found, autoindex will take over
        index index.html index.htm; 
    }
}
```



### Test and Restart

**Test the configuration syntax**

```bash
sudo nginx -t
```

Ensure the output confirms: `syntax is ok` and `test is successful`.

**Restart the Nginx service**

```bash
sudo systemctl restart nginx
```



## Troubleshooting

If you cannot access your file server at `http://your_server_ip:10000/`, it is almost certainly due to one of the following reasons.

### Firewall Configuration

If the web server is running but the page times out or refuses connection, your firewall is likely blocking port `10000`.

**Option A: Open the Specific Port (Recommended)**

```bash
sudo ufw allow 10000/tcp
sudo ufw status
```

**Option B: Disable the Firewall (For Testing Only)**

To quickly confirm that the firewall is the issue, you can temporarily disable UFW. Do not leave the firewall disabled on production servers.

```bash
sudo ufw disable
sudo ufw status
```



### Nginx Main Configuration Check

While placing files in `conf.d/` is generally correct, it only works if the main Nginx configuration file is set to include them.

1. **Check the main config file**

   ```bash
   sudo vim /etc/nginx/nginx.conf
   ```

2. **Verify the include directive**

   Inside the main `http { ... }` block, ensure one of the following lines exists:

   ```nginx
   http{
   	# ...other settings...
   
       include /etc/nginx/conf.d/*.conf;
       include /etc/nginx/sites-enabled/*;
   }
   ```



### Linux File Permissions Fix (The 403 Solution)

If the Nginx configuration is correct, a **403 Forbidden** is almost always a Linux file permission issue.

1. **Check the Nginx Error Log (The Crucial First Step) 🔍** This log will definitively tell you **why** Nginx is blocking the request. Look for `Permission denied` (a file system issue) or `directory index is forbidden` (a missing `autoindex on;` directive).

   ```bash
   sudo tail /var/log/nginx/error.log
   ```

2. **Identify the Nginx User:** Confirm the user Nginx is running as.

   ```bash
   grep "user" /etc/nginx/nginx.conf
   ```

   If it returns `user www-data;` or `user nginx;`, it means Nginx doesn't have enough permission to access the `file_share` folder.

3. **Fix Ownership and Permissions:** If the log showed `(13: Permission denied)`, Nginx cannot read your files. Replace `/srv/file_share` with your actual path, and replace `www-data` with your Nginx user if necessary.

   **Option 1:** Change ownership to the Nginx user

   ```bash
   sudo chown -R www-data:www-data /srv/fileserver/
   ```

   **Option 2:** Set Directory Permissions (755): Read/Execute for all

   ```bash
   sudo find /srv/file_share/ -type d -exec chmod 755 {} \;
   ```

   **Option 3:** Set File Permissions (644): Read-only for Nginx

   ```bash
   sudo find /srv/file_share/ -type f -exec chmod 644 {} \;
   ```

4. **Fix Home Directory Path Permissions (If Applicable):** If your files are in a home folder (e.g., `/home/ubuntu/file_share`), you must allow the Nginx user to traverse the parent directory. Replace `ubuntu` with your username.

   ```bash
   sudo chmod o+x /home/ubuntu/
   ```

   

### Complete All Steps and Restart

After making any changes to permissions, configurations, or the firewall, always test the configuration and restart the service one final time.

```bash
sudo nginx -t
sudo systemctl restart nginx
```

Your file server should now be fully accessible!
