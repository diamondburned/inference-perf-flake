# inference-perf-flake

Create a `flake.nix` file with the following:

```nix
{
  inputs = {
    inference-perf-flake.url = "github:diamondburned/inference-perf-flake";
    inference-perf-flake.inputs.inference-perf.url = ".";
  };

  outputs = { inference-perf-flake, ... }: inference-perf-flake;
}
```

Be sure to add `flake.nix` and `flake.lock` to the repo-local gitignore as well:

```sh
printf '%s\n' flake.{nix,lock} >> .git/info/exclude
```

Available note-worthy flake outputs:

- `devShells.<system>.default` contains tools to develop `inference-perf`
- `packages.<system>.default` contains the `inference-perf` package itself
