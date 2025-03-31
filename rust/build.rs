use std::path::PathBuf;

use std::env;
use std::str;
use glob::glob;

fn check_unstable(proto_path: &PathBuf, build_unstable: bool) -> bool {
    if build_unstable {
        return true;
    }
    let proto_path_str: &str = proto_path.to_str().unwrap();

    return !(proto_path_str.contains("alpha/") || proto_path_str.contains("beta/") || proto_path_str.contains("dev/"));
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

    let mut proto_files: Vec<PathBuf> = Vec::new();
    for file in find_proto_files(proto_dir, build_unstable) {
        proto_files.push(file);
    }

    // Compile rust code for all proto files.
    // You can use .out_dir("./src") to generate code into files for local inspection.
    println!("Generating proto bindings");
    tonic_build::configure()
        .emit_rerun_if_changed(false)
        .include_file("./include.rs")
        .compile(&proto_files, &["./proto"])
        .unwrap();

    // Once protos are built, layer in client adapters.
    Ok(())
}
