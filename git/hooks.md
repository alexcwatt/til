# Hooks

I knew that Git had some hooks like pre-commit, but I learned today about server-side hooks.

I have a Synology NAS that hosts a Git repo and I was able to use a post-receive hook on the server to materialize the repo into a specific folder; this is part of a strategy for hosting a web server on my local network, and I need the server to have access to the latest files in the repo.
