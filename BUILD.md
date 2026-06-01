# Building and Distributing Command Storage

This document outlines the recommended ways to build and distribute the `command-storage` CLI tool to end users to ensure fast installation and avoid cross-platform build issues.

## The Problem with Source Distribution via Homebrew

When building Python applications with C/Rust extensions (like `pydantic-core` and `thefuzz`), distributing via Homebrew's `virtualenv_create` will attempt to build these dependencies from source on the user's machine.

This causes two major issues:
1. **Slow Installations:** Compiling Rust/C code takes a significant amount of time.
2. **Build Failures:** Different architectures (e.g., M1 Apple Silicon vs Intel) might require specific build tools (`rust`, `cmake`), which can lead to installation failures if the environment is not set up perfectly.

## Solution 1: Standalone Executable using PyInstaller (Recommended)

Bundle the Python runtime and all dependencies into a single, standalone executable using PyInstaller. Users can then simply download this single binary via Homebrew and run it without needing Python or any dependencies installed. This avoids Homebrew's network sandbox restrictions during `install` since it only downloads the final binary.

## Solution 2: Instruct users to install via `pipx` directly

Instead of using Homebrew at all, recommend that users install the tool directly using `pipx`. `pipx` is designed for installing Python CLI applications in isolated environments. It prefers downloading pre-compiled binary `.whl` files (wheels) instead of building from source, which drastically reduces installation time and avoids local build issues.

### Building with PyInstaller

1. Install PyInstaller in your development environment:
   ```bash
   poetry add --group dev pyinstaller
   ```

2. Build the executable:
   ```bash
   poetry run pyinstaller --name cmds --onefile command_storage/views/cli.py
   ```

3. The generated executable will be in the `dist/` directory.

### Distributing via Homebrew

Once you have a PyInstaller binary, you can attach it to a GitHub Release (e.g., `cmds-mac-arm64.tar.gz`). Your Homebrew formula can then simply download this binary and place it in the `bin/` directory, avoiding Python and `pip` entirely on the user's machine.

```ruby
class CommandStorage < Formula
  desc "Command-line tool to store CLI commands for quick access and usage"
  homepage "https://github.com/ashu-tosh-kumar/command-storage"
  url "https://github.com/ashu-tosh-kumar/command-storage/releases/download/v0.1.3/cmds-mac-arm64.tar.gz"
  sha256 "<binary_sha256>"

  def install
    bin.install "cmds"
  end
end
```