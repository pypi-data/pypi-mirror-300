# Py Populate Dcim

<!--
Developer Note - Remove Me!

The README will have certain links/images broken until the PR is merged into `develop`. Update the GitHub links with whichever branch you're using (main etc.) if different.

The logo of the project is a placeholder (docs/images/icon-py-populate-dcim.png) - please replace it with your app icon, making sure it's at least 200x200px and has a transparent background!

To avoid extra work and temporary links, make sure that publishing docs (or merging a PR) is done at the same time as setting up the docs site on RTD, then test everything.
-->

<p align="center">
  <img src="https://raw.githubusercontent.com/autonaut/nautobot-app-py-populate-dcim/develop/docs/images/icon-py-populate-dcim.png" class="logo" height="200px">
  <br>
  <a href="https://git.autonaut.dev/autonaut/nautobot-app-py-populate-dcim/actions"><img src="https://git.autonaut.dev/autonaut/nautobot-app-py-populate-dcim/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/py-populate-dcim/en/latest/"><img src="https://readthedocs.org/projects/nautobot-plugin-py-populate-dcim/badge/"></a>
  <a href="https://pypi.org/project/py-populate-dcim/"><img src="https://img.shields.io/pypi/v/py-populate-dcim"></a>
  <a href="https://pypi.org/project/py-populate-dcim/"><img src="https://img.shields.io/pypi/dm/py-populate-dcim"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

> Developer Note: Add a long (2-3 paragraphs) description of what the App does, what problems it solves, what functionality it adds to Nautobot, what external systems it works with etc.

### Screenshots

> Developer Note: Add any representative screenshots of the App in action. These images should also be added to the `docs/user/app_use_cases.md` section.

> Developer Note: Place the files in the `docs/images/` folder and link them using only full URLs from GitHub, for example: `![Overview](https://raw.githubusercontent.com/autonaut/nautobot-app-py-populate-dcim/develop/docs/images/app-overview.png)`. This absolute static linking is required to ensure the README renders properly in GitHub, the docs site, and any other external sites like PyPI.

More screenshots can be found in the [Using the App](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/user/app_use_cases/) page in the documentation. Here's a quick overview of some of the app's added functionality:

![](https://raw.githubusercontent.com/autonaut/nautobot-app-py-populate-dcim/develop/docs/images/placeholder.png)

## Try it out!

> Developer Note: Only keep this section if appropriate. Update link to correct sandbox.

This App is installed in the Nautobot Community Sandbox found over at [demo.nautobot.com](https://demo.nautobot.com/)!

> For a full list of all the available always-on sandbox environments, head over to the main page on [networktocode.com](https://www.networktocode.com/nautobot/sandbox-environments/).

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://git.autonaut.dev/autonaut/nautobot-app-py-populate-dcim/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/py-populate-dcim/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.

## Developing

This Nautobot app uses Poetry to manage its Python environment. Kick off your dev environment by creating and loading into a Python virtual environment with Poetry:
```bash
poetry lock && poetry install && poetry shell
```

After this, `invoke` can be used to start up the development environment. Invoke starts up the required PostgresQL DB and a few Nautobot workers for you using docker-compose.
```bash
invoke destroy && invoke build && invoke start
```

## Dependencies
Two Python packages are included in the app's Poetry configuration (pyproject.toml) as PyPi packages. For development of the dependencies with hot-reload, replace the PyPi package with a directory configuration.