use std::path::{Path, PathBuf};

use std::env;
use glob::glob;

fn check_unstable(proto_path: &Path, build_unstable: bool) -> bool {
    if build_unstable {
        return true;
    }
    let proto_path_str: &str = proto_path.to_str().unwrap();

    !(proto_path_str.contains("alpha/") || proto_path_str.contains("beta/") || proto_path_str.contains("dev/"))
}

fn find_proto_files(proto_dir: &str, build_unstable: bool) -> impl Iterator<Item = PathBuf> {
    let proto_pattern = format!("{}/**/*.proto", proto_dir);
    match glob(&proto_pattern) {
        Ok(iter) => iter
            .map(|item| item.expect("Unable to read file"))
            .filter(move |item| check_unstable(item, build_unstable))
            .map(|item| item.to_owned()),
        Err(err) => panic!(
            "Unable to read proto directory {}: {:?}",
            proto_dir,
            err
        )
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proto_dir = "./proto/sentry_protos";
    println!("Generating protos in {}", proto_dir);

    let build_unstable = match env::var("SENTRY_PROTOS_BUILD_UNSTABLE") {
        Ok(v) => v == "1",
        Err(_) => false,
    };
    let mut build_mode = "stable";
    if build_unstable {
        build_mode = "unstable";
    }
    println!("Building {build_mode} protos");

    let proto_files: Vec<PathBuf> = find_proto_files(proto_dir, build_unstable).collect();

    // Compile proto files and generate a module include file.
    // prost-build's include_file generates properly nested `pub mod`
    // declarations that mirror the proto package hierarchy, ensuring
    // prost's `super::` references resolve correctly.
    println!("Generating proto bindings");
    tonic_prost_build::configure()
        .emit_rerun_if_changed(false)
        .out_dir("./rust/src")
        .include_file("_include.rs")
        .compile_protos(&proto_files, &["./proto".into()])
        .unwrap();

    // Generate lib.rs that re-exports the generated modules,
    // stripping the `sentry_protos` wrapper module so that
    // crate paths are e.g. `sentry_protos::billing::v1::*`
    // rather than `sentry_protos::sentry_protos::billing::v1::*`.
    println!("Generating src/lib.rs");
    std::fs::write(
        Path::new("./rust/src/lib.rs"),
        "include!(\"_include.rs\");\npub use crate::sentry_protos::*;\n"
    )
    .expect("Failed to write lib.rs");

    // Once protos are built, layer in client adapters.
    Ok(())
}
