---
title: All about conda
---


## conda

### What Does `conda config --set channel_priority strict` Do?

The command `conda config --set channel_priority strict` tells Conda to give higher priority to packages from the first-listed channel (in the configuration) and only consider lower-priority channels if a package is **not found** in the higher-priority ones. In **strict** mode, Conda will not pull packages from lower-priority channels if they exist in higher-priority ones, ensuring a more predictable and consistent environment.

- **Strict mode** prevents mixing packages from different channels unless absolutely necessary.
- Without **strict mode**, Conda might pull dependencies from lower-priority channels if it finds a better match (leading to potential inconsistencies).

### What Are Channels in Conda?

A **Conda channel** is a location where packages are stored and distributed. These channels host collections of software packages that can be installed and managed by Conda.

- Channels are typically URLs that point to a repository of packages.
- By default, Conda uses the official **Anaconda repository** (`defaults`) for packages.
- You can add and prioritize other channels, like **conda-forge**, to expand the available package base.

### How Does Conda Work with Channels?

1. **Search for Packages**: When you run a Conda install or update command, Conda looks for the requested package in the configured channels.
2. **Channel Priority**: Channels are evaluated based on the priority defined in your Conda configuration. Higher-priority channels are considered first. If **strict** channel priority is enabled, Conda will not use lower-priority channels if the package exists in the higher-priority channel.
3. **Channels with Packages**: When you install a package, Conda fetches the package and its dependencies from these channels.

### Default Channels in Conda

1. **defaults**: The official channel hosted by Anaconda (Anaconda Distribution). This is the default channel when using Conda.
2. **conda-forge**: A popular community-maintained channel that hosts many packages not available in the defaults channel. Often includes newer versions of packages and a broader selection.

You can list all the configured channels using:
```bash
conda config --show channels
```

### Is Using Conda Channels Safe?

- **Default channels (`defaults`) and `conda-forge`** are widely used, community-supported, and generally safe.
- When using external or third-party channels, always check the trustworthiness of the source.
  
Conda packages are often built from open-source software and are vetted, but users should be cautious when adding new or unknown channels to avoid potential security risks.

### Can I Create My Own Conda Channel Without Paying?

Yes! You can create your own Conda channel **for free**. Here's how it works:

1. **Create a local or hosted repository**:
   - A Conda channel is essentially a directory structure containing packages and metadata (in the form of an `index.html` file).
   - You can create a channel locally on your machine or host it on a web server (even on GitHub, Amazon S3, etc.).

2. **Add Packages to Your Channel**:
   - You can build Conda packages using `conda-build` and move them into your custom channel's directory.
   
3. **Hosting**:
   - **Local Channel**: You can create a local channel by building packages and hosting them in a directory that can be accessed by Conda.
   - **Online Channel**: To make it publicly available, you can host your channel on any public or private server.

4. **Add Your Channel**:
   - You can add your custom channel to Conda’s configuration:
     ```bash
     conda config --add channels <your_channel_url>
     ```

### Example: Creating a Local Channel

1. Create a directory to serve as your channel:
   ```bash
   mkdir -p ~/my-conda-channel/linux-64
   ```

2. Add packages to the `linux-64` folder (or any platform-specific folder).

3. Generate the metadata needed for Conda to index the channel:
   ```bash
   conda index ~/my-conda-channel/
   ```

4. Use the channel:
   ```bash
   conda config --add channels file:///home/user/my-conda-channel/
   ```

You can also upload packages to public channels like **Anaconda Cloud**, but some advanced hosting services may require payment.

### Popular Conda Channels

- **defaults**: Official Anaconda repository.
- **conda-forge**: A community-maintained repository with a broad range of packages.
- **bioconda**: Focuses on bioinformatics software.
- **anaconda**: Hosts packages and collections from Anaconda Inc.

These channels are all safe and commonly used for various types of software packages.


## conda and cuda

```
conda config --show channels

conda config --add channels conda-forge
conda config --set channel_priority strict


conda search onnxruntime-gpu
conda search cudnn --info
conda search onnxruntime-gpu --info

conda install onnxruntime-gpu
pip install onnxruntime-gpu==<version> --find-links https://download.pytorch.org/whl/cu118
```


## let's say I have a local code repo which I want to build ; create a locally hosted conda channel on my machine and then publish this built package to locally hosted conda channel; and the install it on the other machine; in order to prevent unauthorised access, want to protect with seprate username and password then the system on which conda channel is hosted? is this possible? provide detail explainations and step by step for these from building publishing, configuration, and installation, end to end perspective

Yes, it's possible to set up a locally hosted Conda channel with package protection using username and password authentication. This can be done using web servers (e.g., NGINX, Apache) to serve the Conda channel and secure it with basic authentication.

Here’s a detailed step-by-step guide from building the package, creating a locally hosted Conda channel, publishing the package to the channel, protecting the channel with basic authentication, and installing the package on another machine.

---

## 1. Build the Conda Package Locally

### Prerequisites:
- `conda-build`: Install it if not already done.
  ```bash
  conda install conda-build
  ```

### Step-by-Step:

1. **Create a Conda Recipe**:
   If you don't have a recipe for the package, you can create one using `conda skeleton` or manually write the `meta.yaml` file.

   Example of `meta.yaml`:
   ```yaml
   package:
     name: mypackage
     version: 0.1.0
   
   source:
     path: ../  # Assuming the source code is in the parent directory

   build:
     number: 0
     script: python setup.py install  # If using Python

   requirements:
     build:
       - python
       - setuptools
     run:
       - python
       - numpy  # Add your runtime dependencies here
   ```

2. **Build the Package**:
   Run the following command to build the package:
   ```bash
   conda build path/to/conda/recipe  # The directory containing meta.yaml
   ```

   After building, the `.tar.bz2` file will be generated in Conda’s build environment (likely under `~/miniconda3/conda-bld/`).

---

## 2. Create a Locally Hosted Conda Channel

1. **Create a Directory for the Channel**:
   Create a directory where the packages will be stored.
   ```bash
   mkdir -p ~/my-conda-channel/linux-64
   ```

2. **Move the Built Package**:
   Copy the package built in the previous step into the `linux-64` directory.
   ```bash
   cp ~/miniconda3/conda-bld/linux-64/mypackage-0.1.0-0.tar.bz2 ~/my-conda-channel/linux-64/
   ```

3. **Index the Channel**:
   Run `conda index` to generate the required metadata.
   ```bash
   conda index ~/my-conda-channel/
   ```

   This creates the `index.html` and `repodata.json` files needed by Conda to recognize this as a valid channel.

---

## 3. Serve the Conda Channel via a Web Server (NGINX)

To serve the Conda channel with basic authentication, use a web server like **NGINX**.

### Install NGINX

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install nginx
  ```

### Configure NGINX to Serve the Conda Channel

1. **Create a Configuration File**:
   Create a new site configuration in NGINX for your Conda channel.
   ```bash
   sudo nano /etc/nginx/sites-available/conda-channel
   ```

2. **Add Configuration for the Conda Channel**:
   Example NGINX configuration for serving the Conda channel and enabling basic authentication:
   ```nginx
   server {
     listen 80;
     server_name your-domain.com;

     location / {
       root /home/youruser/my-conda-channel;
       autoindex on;
       index index.html;
       auth_basic "Protected Conda Channel";
       auth_basic_user_file /etc/nginx/.htpasswd;
     }
   }
   ```

   - `root /home/youruser/my-conda-channel;`: Path to your local Conda channel.
   - `auth_basic`: Enables basic authentication.
   - `auth_basic_user_file`: Path to the password file.

3. **Enable the Site**:
   Link the new configuration to `sites-enabled`.
   ```bash
   sudo ln -s /etc/nginx/sites-available/conda-channel /etc/nginx/sites-enabled/
   ```

4. **Create a Password File**:
   You’ll need to create an `.htpasswd` file to store the username and password for accessing the channel.

   Install `htpasswd` (if not already installed):
   ```bash
   sudo apt install apache2-utils
   ```

   Create the `.htpasswd` file and add a user:
   ```bash
   sudo htpasswd -c /etc/nginx/.htpasswd username
   ```
   You’ll be prompted to enter a password.

5. **Restart NGINX**:
   Restart NGINX to apply the changes.
   ```bash
   sudo systemctl restart nginx
   ```

At this point, your Conda channel should be accessible via `http://your-domain.com` but protected with basic authentication.

---

## 4. Installing the Package on Another Machine

1. **Add the Protected Conda Channel**:
   On the target machine, add the Conda channel by specifying the URL (use HTTPS if SSL is configured).

   ```bash
   conda config --add channels http://username:password@your-domain.com
   ```

   - Replace `username` and `password` with your actual credentials.
   - Replace `your-domain.com` with the actual server address.

2. **Install the Package**:
   Now, you can install the package from your protected channel:
   ```bash
   conda install mypackage
   ```

   Conda will access the protected channel using the provided credentials and install the package.

---

## 5. Conda Channel Configuration for Multiple Machines

If you need to install packages on multiple machines, ensure that the credentials are provided in the Conda configuration or environment variable to avoid storing them in plain text. For example, you can use `HTTP_PASSWORD` and `HTTP_USERNAME` environment variables in your system:

```bash
export HTTP_USERNAME="your_username"
export HTTP_PASSWORD="your_password"

conda config --set proxy_servers.http http://$HTTP_USERNAME:$HTTP_PASSWORD@your-domain.com
```

This way, you avoid directly exposing credentials in the command line.

---

### Conclusion

1. **Building and Publishing**:
   - Build the package locally using `conda-build`.
   - Create a local Conda channel by organizing your built packages in a directory and using `conda index`.

2. **Serving the Channel**:
   - Use NGINX (or another web server) to serve the channel, and secure it with basic authentication using `.htpasswd`.

3. **Installing on Another Machine**:
   - Add the protected channel to the Conda configuration.
   - Install the packages using credentials for authorized access.

This setup provides a secure, self-hosted Conda channel that can be used internally across multiple machines while protecting it with username/password authentication.


## can I also publish the locally created channel for community like the pip packages to pypi; but then to a separate dedicated channgel for open source oranization

Yes, you can publish your locally created Conda channel and make it publicly available to the community, similar to how packages are published on PyPI for Python packages. However, Conda does not have a centralized repository like PyPI for packages; instead, it uses various **channels**, which are collections of packages. 

You can create a dedicated Conda channel for your open-source organization, host it on a service like **Anaconda.org**, or self-host it on your own infrastructure. Here's how you can set up both options:

---

## 1. Publish Your Conda Packages on Anaconda.org

### Anaconda.org Overview
Anaconda.org is a public platform where you can host and share Conda packages. You can create an organization and publish your packages to a dedicated channel that anyone can use.

### Step-by-Step Guide:

1. **Create an Account**:
   - Go to [Anaconda.org](https://anaconda.org/) and create a free account if you don’t already have one.

2. **Create an Organization**:
   - Once logged in, you can create an organization for your open-source project. Organizations allow multiple users to publish packages under a shared namespace.

   - Go to the **Organizations** tab and click **Create Organization**.
   - Fill in the necessary details and configure the organization as needed.

3. **Install `anaconda-client`**:
   - Install the `anaconda-client` tool to interact with Anaconda.org from the command line.
     ```bash
     conda install anaconda-client
     ```

4. **Log in to Anaconda.org**:
   - Log in using your Anaconda.org credentials:
     ```bash
     anaconda login
     ```

5. **Upload the Package to Your Organization's Channel**:
   - Once logged in, you can upload your package to your organization's channel.
     ```bash
     anaconda upload -u <organization_name> <path_to_your_conda_package>
     ```

   - The `-u` flag is used to specify the organization where you want to upload the package.

6. **Make Your Channel Public**:
   - After uploading, ensure that your organization's channel is public so others can install your packages. You can manage this in the **Settings** of your organization on Anaconda.org.

7. **Share the Channel**:
   - Once the package is uploaded, others can use your channel by adding it to their Conda configuration:
     ```bash
     conda config --add channels https://conda.anaconda.org/<organization_name>
     ```

   - Now, they can install your package like this:
     ```bash
     conda install <package_name>
     ```

---

## 2. Publish via a Self-Hosted Dedicated Channel for the Open-Source Organization

If you prefer to manage and host your own Conda packages without using Anaconda.org, you can set up a dedicated Conda channel on your own infrastructure. This option gives you full control over the hosting, distribution, and security of your packages.

### Step-by-Step Guide:

### 1. **Build and Organize Your Packages Locally**:
   - Use `conda-build` to build your packages locally, as described in the earlier steps.
   - Organize the built packages into platform-specific directories, such as `linux-64`, `osx-64`, `win-64`, etc.

     Example directory structure:
     ```
     ~/conda-channel/
     ├── linux-64/
     │   ├── mypackage-0.1.0-0.tar.bz2
     │   └── index.json
     ├── osx-64/
     │   ├── mypackage-0.1.0-0.tar.bz2
     │   └── index.json
     ```

2. **Serve the Channel via a Web Server**:
   - You can host the Conda channel on your own infrastructure (cloud server, VPS, etc.) and make it available over the internet.
   - Use **NGINX** or **Apache** as the web server to serve the packages (as previously shown).
   - Ensure the Conda channel is publicly accessible (no need for basic authentication unless you want restricted access).

3. **Index the Channel**:
   After organizing the packages, use `conda index` to create the metadata needed for Conda to recognize the channel.
   ```bash
   conda index ~/conda-channel/
   ```

4. **Distribute the Channel URL**:
   - Once your web server is set up and serving the packages, you can distribute the URL to your community.
   - Users can add your channel to their Conda configuration:
     ```bash
     conda config --add channels https://your-domain.com/conda-channel
     ```

5. **Install Packages from the Channel**:
   Users can now install packages from your hosted channel:
   ```bash
   conda install mypackage
   ```

---

## 3. Protecting Your Channel with Username and Password

If you want to limit access to your hosted Conda channel (e.g., for paid access or restricted open-source distribution), you can protect it with basic authentication (as shown earlier with NGINX).

- **NGINX Configuration for Basic Authentication**:
   ```nginx
   server {
     listen 80;
     server_name your-domain.com;

     location / {
       root /home/youruser/conda-channel;
       autoindex on;
       index index.html;
       auth_basic "Protected Conda Channel";
       auth_basic_user_file /etc/nginx/.htpasswd;
     }
   }
   ```

- **Create `.htpasswd` File**:
   ```bash
   sudo htpasswd -c /etc/nginx/.htpasswd username
   ```

Now, only users with the username and password will be able to access the Conda channel.

---

## 4. Automating Package Distribution via CI/CD

If you want to continuously publish packages to your Conda channel (either Anaconda.org or your self-hosted channel), you can integrate CI/CD pipelines to automate the process. Tools like GitHub Actions, GitLab CI, or Jenkins can be used to:

- Build the package automatically on code changes.
- Push the package to the Conda channel (either self-hosted or Anaconda.org).
  
For Anaconda.org:
- Use the `anaconda-client` CLI in your CI pipeline to upload packages directly.

For a self-hosted solution:
- Automate the `conda build`, `conda index`, and file transfer processes to your server.

---

## Conclusion

- **Anaconda.org** provides a straightforward way to publish and share Conda packages with the community by hosting your own organization's channel.
- Alternatively, **self-hosted Conda channels** give you full control and flexibility to manage your own distribution.
- Protecting your channel with authentication ensures restricted access if needed.
- With automation, you can integrate CI/CD for continuous delivery of packages to your open-source community.

Both methods allow you to distribute your Conda packages effectively to your community while maintaining control over security and distribution methods.


## what is the best way to make this build conda package available on cloud platform where it is being used by my app as a librarly or cli on cloud so it is accessbile to over internet; like the choice of using github or gitlab as gitops directly integrating with say AWS and seprately publish on conda channel; or to CI/CD to conda channel and then from there to CI.CD to AWS; or treat these two publishing as seprate deliverables and end consumer - one is to make it accessible to conda community and then other is to hae it deployed as app for accessing over internet in hosted environemnt; what process is efficient and remmended best practice in the industry
