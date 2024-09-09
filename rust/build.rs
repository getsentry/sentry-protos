use std::path::PathBuf;

use std::fs;
use std::fs::File;
use std::io::Write;
use std::str;
use glob::glob;
use regex::Regex;

#[derive(Clone, Debug)]
struct ModuleInfo {
    name: String,
    version: String,
    path: String,
}

fn find_proto_files(proto_dir: &str) -> impl Iterator<Item = PathBuf> {
    let proto_pattern = format!("{}/**/*.proto", proto_dir);
    match glob(&proto_pattern) {
        Ok(iter) => iter
            .map(|item| item.expect("Unable to read file"))
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

    // collect module names to generate lib.rs
    let mut module_metadata = Vec::new();
    let mut proto_files: Vec<PathBuf> = Vec::new();
    for file in find_proto_files(proto_dir) {
        module_metadata.push(get_module_info(&file));
        proto_files.push(file);
    }

    // Compile rust code for all proto files.
    // You can use .out_dir("./src") to generate code into files for local inspection.
    println!("Generating proto bindings");
    tonic_build::configure()
        .emit_rerun_if_changed(false)
        .compile(&proto_files, &["./proto"])
        .unwrap();

    let mut visited: Vec<&str> = vec![];
    let mut lib_rs = String::new();
    for module in module_metadata.iter() {
        if visited.iter().any(|i| i.contains(&module.path)) {
            continue;
        }
        visited.push(module.path.as_str());

        // TODO find a better way to generate this code
        lib_rs.push_str(format!("pub mod {} {{\n", module.name).as_ref());
        lib_rs.push_str(format!("    pub mod {} {{\n", module.version).as_ref());
        lib_rs.push_str(format!("       tonic::include_proto!(\"{}\");\n", module.path).as_ref());
        lib_rs.push_str("   }\n");
        lib_rs.push_str("}\n");
        lib_rs.push_str("\n");
    }

    // Generate lib.rs with the proto modules.
    println!("Generating src/lib.rs");
    let mut lib_file = File::create("./src/lib.rs").unwrap();
    lib_file.write_all(lib_rs.as_bytes()).expect("Failed to write lib.rs");

    // Once protos are built, layer in client adapters.
    Ok(())
}

fn get_module_info(path: &PathBuf) -> ModuleInfo {
    let file = fs::read(path);
    let Ok(contents) = file else {
        panic!("Could not read {:?}", path);
    };
    let contents_str = str::from_utf8(&contents).unwrap();
    let pattern = Regex::new(r"(?m)^package\s+(?<name>[^;]+);").unwrap();
    let Some(captures) = pattern.captures(contents_str) else {
        panic!("Could not find package name in {:?}", path);
    };
    let package_name = captures["name"].to_string();
    let mut parts = package_name.split('.');

    let version = parts.nth_back(0).unwrap().to_string();
    let name = parts.nth_back(0).unwrap().to_string();

    ModuleInfo {name, version, path: package_name}
}
