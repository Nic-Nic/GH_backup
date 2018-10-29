# GitHub backup

This script allows the user to download and/or pull all repositories of a given
user or organization (according to their permissions).

**Author:**  | Nicolàs Palacio-Escat
------------ | --------------------------
**Contact:** | nicolaspalacio91@gmail.com


## Installation

The script does not require any installation. The only thing needed is Python
and the `pycurl` package.

In order to be able to access the private repositories of the user/organization,
a valid user name and token is needed.

## Usage

From a Terminal, type:

```bash
$ python -u GH_backup.py <your_github_registered_email> <path_to_token_file> <orgs|users>/<org/user_name>
```

The option `-u` is optional, it only avoids the buffering of standard output.

The script basically makes a request to GitHub API for the list of repositories
from the given user or organization. Then for each one of them, checks for an
existing folder. If there is, just pulls all the branches, otherwise, creates
the folder and clones the whole repository (including all branches).

### Examples

Imagine you want to download all repositories from the Atom organization.
Assuming the script and the token files are in your current directory:

```bash
$ mkdir Atom
$ cd Atom
$ python -u ../GH_backup.py my_gh_email@somewhere.com ../my_token.txt orgs/Atom
```

One may for instance create a bash script with pre-defined options in order to
run a backup periodically while saving a log file like this:

```bash
python -u ../GH_backup.py my_gh_email@somewhere.com ../my_token.txt orgs/Atom 2>&1 | tee my_log_file.txt
```

### Where to get the token

In your GitHub user settings, go to "Developer settings" -> "Personal access
tokens" and there, generate a new token with the proper access scopes.

Once created, copy the key into a file and save it.

**IMPORTANT NOTE:** Treat your token as if it were a password, as it can grant access to any of the scopes selected on its creation.
