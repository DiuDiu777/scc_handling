# Usage Guide

Here is the steps to run this tool on a Rust Crate.

You must use a Linux OS environment to use the install script. And your OS should have installed rustc and cargo.

You can run `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` to install Rust.

1. Open this project in a terminal. Run `./install.sh`.
2. Open the chosen Rust Crate in the terminal, use `cargo rapx -alias` to perform our alias analysis, or use `cargo rapx -alias-mfp` to perform our maximal fixed-point alias analysis.
