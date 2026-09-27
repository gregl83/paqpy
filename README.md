[![Build](https://github.com/gregl83/paqpy/actions/workflows/release.yml/badge.svg)](https://github.com/gregl83/paqpy/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/paqpy.svg)](https://pypi.org/project/paqpy/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/gregl83/paqpy/blob/master/LICENSE)

# paqPy

Hash directory or file with `BLAKE3`.

Python bindings to the Rust `paq` library.

## Performance

The [Go](https://github.com/golang/go/commit/6e676ab2b809d46623acb5988248d95d1eb7939c) programming language repository was used as a test data source (157 MB / 14,490 files).

| Tool                       | Version | Command                      |     Mean [ms] | Min [ms] | Max [ms] |     Relative |
| :------------------------- | :------ | :--------------------------- | ------------: | -------: | -------: | -----------: |
| [paq][paq]                 | 2.0.0   | `paq ./go`                   |    73.8 ± 0.3 |     73.4 |     74.5 |         1.00 |
| [merkle_hash][merkle_hash] | 3.9.0   | `merkle-hash ./go`           |    98.3 ± 1.0 |     97.2 |    101.0 |  1.33 ± 0.01 |
| [b3sum][b3sum]             | 1.5.1   | `find ./go ... b3sum`        |  318.8 ± 10.2 |    304.0 |    340.7 |  4.32 ± 0.14 |
| [checksumdir][checksumdir] | 1.3.0   | `checksumdir -a sha256 ./go` |   453.1 ± 6.5 |    446.5 |    470.6 |  6.14 ± 0.09 |
| [dirhash][dirhash]         | 0.5.0   | `dirhash -a sha256 ./go`     |   574.9 ± 6.5 |    566.2 |    589.7 |  7.79 ± 0.09 |
| [GNU sha2][gnusha]         | 9.11    | `find ./go ... sha256sum`    |  702.0 ± 34.2 |    661.6 |    793.4 |  9.51 ± 0.46 |
| [folder-hash][folder-hash] | 4.1.1   | `folder-hash ./go`           | 1847.0 ± 40.0 |   1786.0 |   1928.0 | 25.03 ± 0.55 |

[paq]: https://github.com/gregl83/paq
[merkle_hash]: https://github.com/hristogochev/merkle_hash
[checksumdir]: https://pypi.org/project/checksumdir/
[b3sum]: https://github.com/BLAKE3-team/BLAKE3/tree/master/b3sum
[gnusha]: https://manpages.debian.org/testing/coreutils/sha256sum.1.en.html
[dirhash]: https://github.com/andhus/dirhash-python
[folder-hash]: https://github.com/marc136/node-folder-hash

These are upstream paq CLI benchmarks, not measurements of the Python bindings.
See the [paq 2.0.0 benchmarks](https://github.com/gregl83/paq/blob/v2.0.0/docs/benchmarks.md) documentation for methodology and commands.

## Installation

### Install From PyPI

```bash
pip install paqpy
```

### Install From Repository (Unstable)

Not recommended due to instability of main branch in-between tagged releases.

1. Clone this repository.
2. Run `pip install maturin` to install [maturin](https://pypi.org/project/maturin/).
3. Run `maturin develop --release` from repository root.

### Upgrading to v2

paqpy v2 hashes are incompatible with v1; regenerate stored hashes after upgrading.
See [release notes](https://github.com/gregl83/paq/releases/tag/v2.0.0).

## Usage

```python
import paqpy

from pathlib import Path

source = Path("/path/to/source")
ignore_hidden = True # .dir or .file
source_hash = paqpy.hash_source(source, ignore_hidden, follow_links=False)

print(source_hash)
```

`hash_source(source, ignore_hidden, follow_links=False)` returns a hexadecimal
hash string. Existing two-argument calls remain supported. By default, symbolic
links are hashed by their target-path text, including when the source itself is
a symbolic link. Set `follow_links=True` to hash target contents and traverse
linked directories, including targets outside the source tree. Broken links and
cycles raise errors when following links.

`hash_source` uses paq’s fallible Rust API and translates errors into Python
exceptions. File system failures raise the
corresponding Python `OSError` subclass, such as `FileNotFoundError` or
`PermissionError`. Invalid UTF-8 paths raise `UnicodeError`, invalid source
relationships raise `ValueError`, and other hashing failures raise
`paqpy.PaqError`.

Visit the [paq](https://github.com/gregl83/paq) homepage for more details.

## License

[MIT](LICENSE)
