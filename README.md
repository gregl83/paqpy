[![Build](https://github.com/gregl83/paqpy/actions/workflows/release.yml/badge.svg)](https://github.com/gregl83/paqpy/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/paqpy.svg)](https://pypi.org/project/paqpy/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/gregl83/paqpy/blob/master/LICENSE)

# paqPy

Hash directory or file with `BLAKE3`.

Python bindings to the Rust `paq` library.

## Performance

The [Go](https://github.com/golang/go/commit/6e676ab2b809d46623acb5988248d95d1eb7939c) programming language repository was used as a test data source (157 MB / 14,490 files).

| Tool                                     | Version | Command                                 |     Mean [ms] | Min [ms] | Max [ms] |     Relative |
| :--------------------------------------- | :------ | :-------------------------------------- | ------------: | -------: | -------: | -----------: |
| [paq][paq]                               | 2.0.0   | `paq ./go`                              |    31.0 ± 0.4 |     30.4 |     31.7 |         1.00 |
| [merkle_hash][merkle_hash]               | 3.9.0   | `merkle-hash ./go`                      |  120.3 ± 29.6 |     41.0 |    161.9 |  3.88 ± 0.95 |
| [b3sum][b3sum]                           | 1.5.1   | `find ./go ... b3sum`                   |   372.2 ± 9.5 |    357.9 |    386.0 | 12.00 ± 0.34 |
| [directory-checksum][directory-checksum] | 1.4.20  | `directory-checksum --max-depth=0 ./go` |   388.1 ± 3.1 |    382.0 |    393.8 | 12.51 ± 0.18 |
| [GNU md5sum][gnumd5]                     | 9.11    | `find ./go ... md5sum`                  |   398.8 ± 3.0 |    393.7 |    403.5 | 12.85 ± 0.18 |
| [checksumdir][checksumdir]               | 1.3.0   | `checksumdir -a sha256 ./go`            |   454.4 ± 7.9 |    443.1 |    469.9 | 14.64 ± 0.31 |
| [dirhash][dirhash]                       | 0.5.0   | `dirhash -a sha256 ./go`                |   569.8 ± 5.2 |    561.9 |    581.8 | 18.36 ± 0.27 |
| [GNU sha2][gnusha]                       | 9.11    | `find ./go ... sha256sum`               |   661.5 ± 8.7 |    650.4 |    682.2 | 21.32 ± 0.38 |
| [folder-hash][folder-hash]               | 4.1.1   | `folder-hash ./go`                      | 1406.0 ± 62.0 |   1302.0 |   1575.0 | 45.29 ± 2.08 |
| [Hashrat][hashrat]                       | 1.25    | `hashrat -sha256 -dir -hidden ./go`     | 2095.0 ± 34.0 |   2061.0 |   2200.0 | 67.52 ± 1.35 |

[paq]: https://github.com/gregl83/paq
[merkle_hash]: https://github.com/hristogochev/merkle_hash
[directory-checksum]: https://github.com/MShekow/directory-checksum
[hashrat]: https://github.com/ColumPaget/Hashrat
[checksumdir]: https://pypi.org/project/checksumdir/
[b3sum]: https://github.com/BLAKE3-team/BLAKE3/tree/master/b3sum
[gnumd5]: https://www.gnu.org/software/coreutils/manual/html_node/md5sum-invocation.html
[gnusha]: https://manpages.debian.org/testing/coreutils/sha256sum.1.en.html
[dirhash]: https://github.com/andhus/dirhash-python
[folder-hash]: https://github.com/marc136/node-folder-hash

These are upstream paq CLI benchmarks, not measurements of the Python bindings.
The benchmark VM is an AWS EC2 `c6a.4xlarge` (16 vCPUs, 32 GiB RAM).
See the [paq benchmarks](https://github.com/gregl83/paq/blob/main/docs/benchmarks.md) documentation for methodology and commands.

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
