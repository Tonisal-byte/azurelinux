import argparse
import os
import shutil
import subprocess


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
        shutil.copy(os.getcwd()+"/scripts/generate_source_tarball.sh", build_dir)
        
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
            for line in f:
                if "Version:" in line:
                    pkg_version = line.split()[1]
                    break
        if not pkg_version:
            raise Exception("Version not found in spec file")
    except Exception as e:
        print("Error getting package version: ", e)

    # Generates vendored source code
    print("Generating new vendored version of source code...")
    try:
        tar_ball_path = (os.listdir(os.path.join(os.getcwd(),"build",spec_name))).filter(lambda x: x.endswith(".tar.gz"))
        if len(tar_ball_path) == 0:
            raise Exception("No tarball found in package directory")
        subprocess.call([
            './generate_source_tarball.sh',
            '--srcTarball', tar_ball_path[0],
            '--outFolder', os.path.join(os.getcwd(),"build",spec_name),
            '--pkgVersion', pkg_version,
            '--pkgName', spec_name
        ])
    except OSError as e:
        print("Error generating vendored source code: ", e)
    print("Generated vendored source code and packaged @ ", os.path.join(os.getcwd(),"build",spec_name))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a spec file to a Rust build script")
    parser.add_argument("--create-spec",nargs=2, help="Creates a spec file, for the user to fill in parts of the spec file.")
    parser.add_argument("--compile", nargs=1, help="Compiles Rust package using vendored sources and provides all resources to replicate the build.")
    args = parser.parse_args()

    if args.create_spec:
        create_spec_file(args.create_spec[0], args.create_spec[1])
    
    elif args.compile:
        compile_rust_build_script(args.compile[0])

