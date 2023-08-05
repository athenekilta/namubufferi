# Recommended Development
I highly encourage you to use [Visual Studio Code](https://code.visualstudio.com/) as your IDE as it is the one I use and it has a lot of nice features for Python development and some scripts I share here. Create a .vscode folder in the root of the project and add the following files:


- Tasks.json
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "tailwind",
            "type": "shell",
            "command": "python",
            "args": [
                "manage.py",
                "tailwind",
                "start"
            ],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "tests",
            "type": "shell",
            "command": "python",
            "args": [
                "manage.py",
                "test"
            ],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
    ]
}
```
From now on, you can run the following commands from the command palette (Ctrl+Shift+P) in VSCode:
- `Tasks: Run Task` -> `tailwind`
- `Tasks: Run Task` -> `tests`

- settings.json
```json
{
    "terminal.integrated.env.windows": {
        "MOBILEPAY_TOKEN": "<SECRET>",
        "MOBILEPAY_PAYMENTPOINTID": "<SECRET>",
        "NPM_BIN_PATH": "C://Program Files//nodejs//npm.cmd",
    },
    "terminal.integrated.env.osx": {
        "MOBILEPAY_TOKEN": "<SECRET>",
        "MOBILEPAY_PAYMENTPOINTID": "<SECRET>",
    },
    "terminal.integrated.env.linux": {
        "MOBILEPAY_TOKEN": "<SECRET>",
        "MOBILEPAY_PAYMENTPOINTID": "<SECRET>",
    }
}
```

- launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
            ],
            "django": true
        }
    ]
}
```
From now on, just press F5 to start the server in debug mode and use the reddot to set breakpoints. ;)