### Azure Linux Rust Package Converter (AZL-RPC) Documentation

 - **Goals:**
    - Create a tool to aid in the conversion of open source rust packages to SPEC files + resources(i.e. source code) 
    - Minimize the time it takes for an engineer to implement rust packages in Azure Linux (using Build Tools)

- **Workflow**
    - User will create a new template directory via the **--create-spec** command which will take two arguments 1.(package name) 2.(source tarball directory ***abs path***). This command will populate a new directory under the build directory where the user will find the template spec file (now named after the package) to fill out. Additionally, there will be a script to generate a vendored source tarball and the original source tarball included in the new directory. In this build directory there can exsist various rust packages in different stages of conversion from pre-compiled to actively maintained and updated. 

    - The User will typically only need to fill out basic information for the new package like name, version, license, etc (***All of which are clearly marked***). The prep, build, and install sections of the spec file are generalized and work for most packages, if errors occur or additional specificity is needed, alterations can be made to the spec file. 

    - After User fills out the spec file accordingly (to their specification), they will run the **--generate-resources** command which takes only one argument (package name). This will ensure only the target package is compiled. This command will derive information from the spec file and call a seperate (generate_source_tarball.sh) script to create a new source tarball using vendored sources. This command will also update the spec file to include the name of the new tarball and the old tarball.

    - After both command are successfully ran, there should be four items in a completed package build (generate tarball script, old source code tarball, new vendored tarball, new spec file). The User can implement this new package in their build image if they copy the directory and place it in their mariner workspace (***/CBL-Mariner/SPECS***) and update the cgmanifest (***/CBL-Mariner/cgmanifest.json***). 

    - Following the typical Azure Linux Build tool commands should result in a built rpm package after implementation. 

    - Additional functionality to be implemented includes a **--update** command that will recreate the vendored source tarball with updated packages if needed later in the development cycle.

- **Tutorial**
    - Given rust package X, we need to convert this package into the appropriate resources to work with Azure Linux. These resources (along with their file formats) are as follows: SPEC (.spec), package signatures (.json), original source tar (.tar.gz), and vendored tarball (.tar.gz). The aforementioned vendored tarball is a generated resource that compiles the source code and necessary cargo (buildtime) dependencies. Below are the steps to use AZL-RPC to go from package X to AZL package. 

    1.  **Initializing Build:**First we must intialize the project and copy the correct tarball into the newly generated build for package X. By running the `python3 converter.py --create-spec {PACKAGE X NAME} {PACKAGE X SOURCE TARBALL PATH}` we successfuly intialize the package conversion by creating a new directory in the build directory with a template SPEC and a copied version of the tarball. ***Note: make sure to keep the package name consistent throughout this process.***

    2.  **Filling in the SPEC:**After running the first command you are required to fill in some fields of the template SPEC file (labled `{pkgX}.spec`). The user must fill in the Summary, Name, Version, License, URL, Description, Files, and Changelog fields. All fields you are required to fill in are clearly marked on the template. This template is meant to generalize the installation process for the most basic packages. Some packages require a different set of installation instructions, consult package X docs for further guidance. 

    3.  **Generating Resources:**To generate the rest of the resources you will run `python3 converter.py --generate-resources {PACKAGE X NAME}`. This will prompt the tools to generate the vendored source tarball (`{PACKAGE X}-{version}-{vendored}.tar.gz`) and the sinatures for the tarballs (`{PACKAGE X}.signatures.json`). These resources are all that you will need to implement package X. 

    4.  **Implementing Package in AZL:**To implment your newly converted rust package, copy your packageX directory in the build directory and place it in your workspace AZL SPEC folder (***/CBL-Mariner/SPECS***). Next you will want to navigate to the cgmainfest.json file in your AZL workspace (***/CBL-Mariner/cgmanifest.json***) and place you new package (in alphabetical order) as a new object in the manifest. Finaly, you can build your package using our build tools (Ex: `sudo make build-packages ...`).

    5. **Debugging:**Theres a high likely hood that there will be error when first trying to build your new package. This will most likely come from errors in installation location, Requirements, and/or missing files. Some inherent knowledge about package is required to fix these issues. Consult your package's documentation for guidance on building from source code (and be persistent). 