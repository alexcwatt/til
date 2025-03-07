# Dev Containers

[Dev Containers](https://containers.dev/) are containers that facilitate software development. They make it easy to set up a development environment, especially through integration with an editor. I use them with VS Code ([see docs](https://code.visualstudio.com/docs/devcontainers/containers)) to make it easy to spin up the correct development environment for any project:

* I use one for developing my personal website.
* I use one for my [personal finance with Beancount](https://alexcwatt.com/beancount/).
* I use them for my Rails apps.

They are especially valuable when collaborating with others. I have one Rails app where I work with another developer and the devcontainer allows us both to share the same environment setup.

Here are the features I use the most:

* Custom Dockerfile: I'm able to build an image that installs things that I change infrequently: programming language, system dependencies (e.g., something like libvips-dev), etc. Usually my base image is one that was built for the language I am using (e.g., `mcr.microsoft.com/vscode/devcontainers/python:3.13`).
* Docker Compose: For apps where I have dependencies running in other containers (e.g., Postgres, Elasticsearch), I I let the devcontainer.json manage a Docker Compose configuration.
* VS Code Extensions: If there are some extensions that I use for my project, I specify these too, so they install every time.
* Mounts: If my container needs access to my file system, I configure mounts.
* Post-create command (`postCreateCommand`): If specified, this command is invoked after the container boots. I have this call a `bin/setup` script; this does things like install 
