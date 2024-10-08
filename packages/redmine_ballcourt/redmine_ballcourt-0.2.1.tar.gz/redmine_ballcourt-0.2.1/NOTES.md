# Development and publishing notes

* Enable a virtualenv, e.g. with `uv venv` and `source .venv/bin/activate`

* Make sure it's up to date with `uv sync`.

* Create, if you haven't got one, a configuration file, probably in the current directory - see the docs.

* Run the script with, e.g. `uv run -- redmine-ballcourt -n`.

* Build the package with `uv build`.

* Publish the package with `uv publish`.  To the test.pypi.org site, you can use:
    ```bash
    uv publish --token TOKEN --publish-url https://test.pypi.org/legacy/
    ```
    To the real pypi.org site, you can use:
    ```bash
    uv publish -- --publish-url https://upload.pypi.org/legacy/
    ```
    You will need to have a `.pypirc` file in your home directory with your credentials.  You can use the `uv pypirc` command to create this file.

