# white duck Project Scaffolding Tool

https://whiteduck.de/

A tool for scaffolding d python projects with the recommended tech stack of white duck


## Installation

Requirements: python >= 3.10

```bash
pip install whiteduck
```

update

```bash
pip install -U whiteduck
```

## Commands

### Wizard

Run without any parameter

```bash
whiteduck
```

### Create a New Project

```bash
whiteduck create [--template TEMPLATE_NAME] [--output OUTPUT_PATH]
```

`--template` (optional): The name of the template to use. Defaults to the `shiny-default` template.

`--output` (optional): The output path for the new project. Defaults to `.` (current directory).


### List Available Templates

```bash
whiteduck list-templates
```

### Display Template Information

```bash
whiteduck template-info TEMPLATE_NAME
```


## Templates

Naming convention: `{main-framework}-{use case}` (eg. `shiny-default`, `gradio-azureopenai`, `gradio-semantickernel`, etc.)

Available templates

### shiny-default

This template provides boilerplate for a small shiny application, with everything needed to get going quickly.

- deployment via docker
- quick run powershell and bash script
- vscode settings for debugging and formatting
- Classic modular service-based app architecture/structure
- Dependency Injection Container
- Appsettings support
- logging preconfigured



