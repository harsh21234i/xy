---
title: Installation
description: Install XY, understand its bundled runtime, and choose optional integrations.
---

# Installation

XY 0.0.1 supports Python 3.11 and newer. Install the released core package
from PyPI with your preferred package manager:

~~~~md tabs
## uv

~~~bash
uv add xy
~~~

## pip

~~~bash
python -m pip install xy
~~~
~~~~

Confirm the package imports from the environment where your code will run:

~~~bash
python -c "import xy; print(xy.__version__)"
~~~

## Supported platforms

Prebuilt native wheels are published only for targets that the release
workflow can install, load, and exercise on a matching hosted runner.

| Platform | Compatibility | Architecture | Release artifact |
| --- | --- | --- | --- |
| Linux | glibc (`manylinux_2_17`) | `x86_64` | Included; runtime verified |
| macOS | macOS 11+ on Apple silicon | `arm64` | Included; runtime verified |
| Windows | Native Windows | `x86_64` | Included; runtime verified |
| WebAssembly | Pyodide 314 (Emscripten, PEP 783) | `wasm32` | PyEmscripten wheel; runtime verified |

Other architectures and operating systems may be buildable from source with a
compatible Rust toolchain, but are not part of the published wheel matrix until
the release workflow can run an install and native-kernel smoke test for them.

The runtime-verified WebAssembly wheel targets the standardized PEP 783
`pyemscripten_2026_0_wasm32` platform and is published alongside the native
wheels. In-browser Python installs it by package name —
`micropip.install("xy")`, or `%pip install xy` in a JupyterLite notebook.
This target runs XY's Python and Rust core inside Pyodide; it is separate
from the JavaScript/WebGL client included with every chart. See
[Notebooks](/docs/xy/integrations/notebooks/) for how charts display on WASM
kernels.

## What the package includes

The regular `xy` dependency already includes NumPy and anywidget support.
Published platform wheels bundle the Python package, browser client, and native
Rust compute core. Notebook display and HTML, native PNG, and SVG export do not
require separate `notebooks` or `export` extras, Node, npm, or a CDN.

## Installing from Git or source

Use the PyPI wheel when your platform is supported. A working source install
must compile the native compute core, so it requires a Rust toolchain with
`cargo` and `rustc`. The browser client is committed to the repository; Node
and npm are not required just to install it.

To reproduce the 0.0.1 release from Git with uv:

~~~bash
uv add "xy @ git+https://github.com/reflex-dev/xy.git@v0.0.1"
~~~

Or install the same tagged source with pip:

~~~bash
python -m pip install "xy @ git+https://github.com/reflex-dev/xy.git@v0.0.1"
~~~

A source build without Rust can finish installing, but it has no compute
backend and fails with an actionable error when a chart first needs native
compute. XY does not silently switch to a slower implementation. Building for
an unsupported operating system or architecture may also require target-specific
Rust tooling beyond the commands above.

## Optional tools and integrations

### Arrow input

Install `pyarrow` separately when you want Arrow-backed input:

~~~bash
uv add pyarrow
~~~

### Reflex integration

The bundled Reflex integration supports state-backed application charts and
remains experimental. Install the extra to select a compatible Reflex
version. With uv:

~~~bash
uv add "xy[reflex]"
~~~

Or with pip:

~~~bash
python -m pip install "xy[reflex]"
~~~

The `xy` wheel already carries the `reflex_xy` integration; the extra adds
only the supported Reflex dependency floor. Pin resolved versions for
production deployments. Continue with the
[Reflex integration guide](/docs/xy/integrations/reflex/) for its current
limitations and setup.

### Optional browser export

Native PNG is the default static raster path and does not launch a browser.
Chromium-based PNG export is optional and discovers Chrome, Chromium, Edge,
or `chrome-headless-shell` on the machine; set `XY_BROWSER` to an executable
path when automatic discovery is not appropriate.

Next, build [your first chart](/docs/xy/overview/first-chart/).
