"""
This file contains the CLI for the chimera package.
"""

import json
import typer


class CommandLoader:
    def __init__(self, command_json_file):
        self.command_json_file = command_json_file
        self.commands = {}

    def load_commands(self):
        """Loads commands from a JSON file."""
        try:
            with open(self.command_json_file, "r") as file:
                self.commands = json.load(file)
        except FileNotFoundError:
            self.commands = {}

    def add_command(self, name, command_func):
        """Adds a dynamic command to Typer."""
        app.command(name)(command_func)

    def register_commands(self):
        """Registers all commands from the loaded JSON."""
        for cmd_name, cmd_data in self.commands.items():

            def command_function():
                typer.echo(f"Executing {cmd_name} with URL: {cmd_data['url']}")
                # Add logic for HTTP requests or other functionality here

            # Register the dynamic command
            self.add_command(cmd_name, command_function)

    def save_commands(self):
        """Saves the current commands to the JSON file."""
        with open(self.command_json_file, "w") as file:
            json.dump(self.commands, file, indent=4)

    def add_new_command(self, name: str, url: str, method: str):
        """Adds a new command to the commands dictionary and saves it."""
        self.commands[name] = {"url": url, "method": method}
        self.save_commands()
        typer.echo(f"Added new command '{name}' with URL '{url}' and method '{method}'")
        self.register_commands()

    def remove_command(self, name: str):
        """Removes a command from the dictionary and saves the updated commands."""
        if name in self.commands:
            del self.commands[name]
            self.save_commands()
            typer.echo(f"Removed command '{name}'")
        else:
            typer.echo(f"Command '{name}' does not exist")


class BasicCommands:
    def __init__(self, loader: CommandLoader):
        self.loader = loader

    def add(self, name: str, url: str, method: str = "GET"):
        """Add a new command dynamically."""
        self.loader.add_new_command(name, url, method)

    def list_commands(self):
        """List all available commands."""
        if self.loader.commands:
            typer.echo("Available commands:")
            for cmd_name, cmd_data in self.loader.commands.items():
                typer.echo(f"- {cmd_name}: {cmd_data['method']} {cmd_data['url']}")
        else:
            typer.echo("No commands available.")

    def remove(self, name: str):
        """Remove a command."""
        self.loader.remove_command(name)


class Cli:
    def __init__(self, app: typer.Typer, basic_commands: BasicCommands):
        self.app = app
        self.basic_commands = basic_commands

    def register_commands(self):
        """Encapsulates all Typer commands within the class."""

        @self.app.command()
        def add(name: str, url: str, method: str = "GET"):
            """Add a new command dynamically."""
            self.basic_commands.add(name, url, method)

        @self.app.command()
        def list():
            """List all available commands."""
            self.basic_commands.list_commands()

        @self.app.command()
        def remove(name: str):
            """Remove a command."""
            self.basic_commands.remove(name)


# Typer app instance
app = typer.Typer()

# Instantiate the loader and load existing commands
loader = CommandLoader("commands.json")
loader.load_commands()
loader.register_commands()

# Instantiate BasicCommands to handle add, list, and remove
basic_commands = BasicCommands(loader)

# Create CommandApp and register commands
command_app = Cli(app, basic_commands)
command_app.register_commands()

if __name__ == "__main__":
    app()
