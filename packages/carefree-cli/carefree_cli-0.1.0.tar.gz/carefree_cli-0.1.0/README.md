A `cli` that helps you manage your `cli` commands.

## Design

Basically, `cfi` aims to help you when:

- you need to run lots of `cli` commands everyday.
- these commands can be divided into several groups, and commands in each group are highly repetitive.

So the implementation of `cfi` is very simple:

- It will prompt you to create `cli` command templates and manage them in hierarchical structures.
- It will prompt you to 'fill' the template with your own parameters when you want to run a command.
- It will printed out the final command for you to copy-paste / run.

## Installation

`carefree-cli` requires `python>=3.8`.

```bash
pip install cfi
```

## Basic Workflow

1. Initialize `cfi`:

```bash
cfi init
```

2. Create a `cli` template:

```bash
cfi add -h
```

3. Fill a `cli` template:

```bash
cfi load -h
```

## Common Usages

> Fun fact: you can add `cfi` template with `cfi` itself!
>
> ```bash
> cfi add 'cfi add \"{template}\" {hierarchy}' cfi_add
> ```

- Get help:

```bash
cfi -h
```

- Install cli completion:

```bash
cfi --install-completion
```

- List templates:

```bash
cfi list -h
```

## Serializations

- Export templates:

```bash
cfi export
```

- Import templates:

```bash
cfi import -h
```
