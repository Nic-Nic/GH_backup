# GitHub backup

This script allows the user to download and/or pull all repositories of a given
user or organization (according to their permissions).

::

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

### Where to get the token

In your GitHub user settings, go to "Developer settings" -> "Personal access
tokens" and there, generate a new token with the proper access scopes.

Once created, copy the key into a file and save it.

**IMPORTANT NOTE:** Treat your token as if it were a password, as it can grant access to any of the scopes selected on its creation.
