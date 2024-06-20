import argparse
import os
import shutil
import subprocess
import hashlib
import json

def create_spec_file(spec_name:str, tarball_path:str):
    # Creates a new package directory, spec file, and copies source tarball

    print("Creating new package directory...")
    try:
        build_dir = os.path.join(os.getcwd(),"build", spec_name)
        os.mkdir(build_dir)
    except OSError as e:
        print("Error creating package directory: ", e)
    print("Created package directory: ", build_dir)
    
    print("Creating template spec file...")
    try:
        file_path = os.path.join(build_dir, spec_name+".spec")
        shutil.copy(os.getcwd()+"/templates/rust-template.spec", file_path)
        
    except OSError as e:
        print("Error creating spec file: ", e)
    print("Created spec file: ", file_path)
    
    print("Copying tarball to package directory...")
    try:
        # Verify tarball exists
        if not os.path.exists(tarball_path):
            raise Exception("Tarball does not exist @ ", tarball_path)
        shutil.copy(tarball_path, build_dir)
    except Exception as e:
        print(e)
    print("Copied tarball to package directory: ", build_dir)

    print('Done!')
    print("\nPlease fill in the spec file with the appropriate information @ ", file_path,"\nAfter completing the spec file run the following command to complete the packaging process: python converter.py --compile")

def compile_rust_build_script(spec_name:str):
    # Gets package version from .spec file
    print("Getting package version from spec file...")
    pkg_version = None
    try:
        with open(os.path.join(os.getcwd(),"build",spec_name,spec_name+".spec"), "r") as f:
            # Get version from spec file
            for line in f:
                if "Version:" in line:
                    pkg_version = line.split()[1]
                    break
        if not pkg_version:
            raise Exception("Version not found in spec file")
    except Exception as e:
        print("Error getting package version: ", e)
        return
    print("Package version: ", pkg_version)
    # Generates vendored source code
    print("Generating new vendored version of source code...")
    try:
        tar_ball_names:list[str] =  [name for name in (os.listdir(os.path.join(os.getcwd(),"build",spec_name))) if name.endswith(".tar.gz")]
        if len(tar_ball_names) != 1:
            raise Exception("More than one or no tarball found in package directory")
        tar_ball_path = os.getcwd()+f"/build/{spec_name}/{tar_ball_names[0]}"
        if not os.path.exists(tar_ball_path):
            raise Exception("No tarball found in package directory")
        verification_code:int = subprocess.call([
            './scripts/generate_source_tarball.sh',
            '--srcTarball', tar_ball_path,
            '--outFolder', os.path.join(os.getcwd(),"build",spec_name),
            '--pkgVersion', pkg_version,
            '--pkgName', spec_name
        ])
        if verification_code != 0:
            raise Exception("Error generating vendored source code")
    except OSError as e:
        print("Error generating vendored source code: ", e)
        return
    print("Generated vendored source code and packaged @ ", os.path.join(os.getcwd(),"build",spec_name))
    
    print("Editing spec file to match vendored source code...")
    spec_file_path = os.getcwd()+f"/build/{spec_name}/{spec_name}.spec"
    with open(spec_file_path, "r") as spec:
        lines = spec.readlines()
    
    with open(spec_file_path, "w") as spec:
        for line in lines:
            if "Source0:" in line:
                spec.write("Source0: "+spec_name+"-"+pkg_version+"-vendored.tar.gz\n")
            elif "Source1:" in line:
                spec.write("Source1: "+"%{url}/archive/refs/tags/v%{version}.tar.gz#/"+tar_ball_names[0]+"\n")
            else:
                spec.write(line)
    print("Edited spec file to match vendored source code successfully")
    
    print("Creating signatures for vendored source code...")
    signature_dict = get_signatures(spec_name)
    
    with open(os.path.join(os.getcwd(),"build",spec_name,spec_name+".signatures.json"), "w") as f:
        json.dump(signature_dict, f)
    print("Created signatures file @ ", os.path.join(os.getcwd(),"build",spec_name,spec_name+".signatures.json"))
    
        
    
def get_signatures(spec_name) -> dict[str,str]:
    # Get signatures for all source code in package directory
    res_dict:dict = {"Signatures":{}}
    tar_ball_names:list[str] =  [name for name in (os.listdir(os.path.join(os.getcwd(),"build",spec_name))) if name.endswith(".tar.gz")]
    
    for tar_ball in tar_ball_names:
        res_dict["Signatures"][tar_ball] = get_sha256sum(os.path.join(os.getcwd(),"build",spec_name,tar_ball))
    return res_dict
  
def get_sha256sum(file_path:str)->str:
    sha256sum_hash = hashlib.sha256()
    
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256sum_hash.update(byte_block)
        return sha256sum_hash.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a spec file to a Rust build script")
    parser.add_argument("--create-spec",nargs=2, help="Creates a spec file, for the user to fill in parts of the spec file.")
    parser.add_argument("--generate-resources", nargs=1, help="Compiles Rust package using vendored sources and provides all resources to replicate the build.")
    args = parser.parse_args()

    if args.create_spec:
        create_spec_file(args.create_spec[0], args.create_spec[1])
    
    elif args.generate_resources:
        compile_rust_build_script(args.generate_resources[0])

