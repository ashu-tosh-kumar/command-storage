class CommandStorage < Formula
  desc "Command-line tool to store CLI commands for quick access and usage"
  homepage "https://github.com/ashu-tosh-kumar/command-storage"

  # Replace with the URL to the pre-compiled binary (e.g. from GitHub Releases)
  # url "https://github.com/ashu-tosh-kumar/command-storage/releases/download/v0.1.3/cmds-mac-apple-silicon.tar.gz"
  # sha256 "<insert_sha256_here>"

  # For cross-platform support using pipx (recommended approach for Typer/Python CLIs in Homebrew)
  url "https://files.pythonhosted.org/packages/6c/30/705eaaf2a54810a2e880dc03d2b3d0f8faaf481e7bbe8a8108c7988e86a3/command_storage-0.1.3.tar.gz"
  sha256 "db7fdb24181307f802e442c0d83c036166cf0a2e2b9799e73549e91fe696e65a"
  license "MIT"

  depends_on "pipx"

  def install
    # Note: Homebrew runs in a restricted network sandbox during `install`.
    # While you can use `pipx` via Homebrew, the recommended approach for Typer apps
    # is to distribute a pre-compiled binary (e.g. using PyInstaller or shiv) as seen
    # in the commented-out `url` above. If using PyInstaller, you can simply do:
    # bin.install "cmds"
  end

  test do
    assert_match "cmds", shell_output("#{bin}/cmds --version")
  end
end
