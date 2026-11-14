"""Generate local host setup for this checkout without replacing existing config."""
import argparse
import json
from pathlib import Path
import sys

from core import ROOT, tool
from agent_store import initialize


def write_new_or_identical(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"Existing configuration differs; merge the prepared fragment manually: {path}")
        return
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT / "build/integration-data")
    parser.add_argument("--dvisvgm", type=Path)
    args = parser.parse_args()
    store = initialize(args.data_root)
    command = str(Path(sys.executable).resolve())
    arguments = [str(ROOT / "agent_server.py"), "--data-root", store["root"]]
    environment = {}
    if args.dvisvgm:
        if not args.dvisvgm.is_file():
            raise ValueError("dvisvgm executable does not exist")
        environment["SCHEMATICA_DVISVGM"] = str(args.dvisvgm.resolve())
    else:
        try:
            environment["SCHEMATICA_DVISVGM"] = tool("dvisvgm")
        except FileNotFoundError:
            pass
    try:
        environment["SCHEMATICA_TECTONIC"] = tool("tectonic")
    except FileNotFoundError:
        pass
    config = "[mcp_servers.schematica-integration]\n" + "command = " + json.dumps(command) + "\nargs = " + json.dumps(arguments) + "\n"
    config += "cwd = " + json.dumps(str(ROOT.parent)) + "\nstartup_timeout_sec = 30\ntool_timeout_sec = 1800\n"
    if environment:
        config += "\n[mcp_servers.schematica-integration.env]\n" + "".join(k + " = " + json.dumps(v) + "\n" for k, v in environment.items())
    output = ROOT / "build/host-setup"
    write_new_or_identical(output / "codex.toml", config)
    claude = {"mcpServers": {"schematica-integration": {"command": command, "args": arguments, "env": environment}}}
    write_new_or_identical(output / "claude-desktop-fragment.json", json.dumps(claude, indent=2) + "\n")
    write_new_or_identical(ROOT.parent / ".codex/config.toml", config)
    print(json.dumps({"codex_project_config": str(ROOT.parent / ".codex/config.toml"),
                      "claude_fragment": str(output / "claude-desktop-fragment.json"),
                      "store": store, "render_tools": sorted(environment),
                      "next": "Reload the trusted project's MCP connection, then verify search in the actual host."}, indent=2))


if __name__ == "__main__":
    main()
