### Azure Linux Rust Package Converter Documentation

 - **Goals:**
    - Create a tool to aid in the conversion of open source rust packages to SPEC files + resources(i.e. source code) 
    - Minimize the time it takes for an engineer to implement rust packages in Azure Linux (using Build Tools)

- **Workflow**
    - User will create a new template directory via the **--create-spec** command which will take two arguments 1.(package name) 2.(source tarball directory ***abs path***). This command will populate a new directory under the build directory where the user will find the template spec file (now named after the package) to fill out. Additionally, there will be a script to generate a vendored source tarball and the original source tarball included in the new directory. In this build directory there can exsist various rust packages in different stages of conversion from pre-compiled to actively maintained and updated. 

    - The User will typically only need to fill out basic information for the new package like name, version, license, etc (***All of which are clearly marked***). The prep, build, and install sections of the spec file are generalized and work for most packages, if errors occur or additional specificity is needed, alterations can be made to the spec file. 

    - After User fills out the spec file accordingly (to their specification), they will run the **--generate-vendored-tar** command which takes only one argument (package name). This will ensure only the target package is compiled. This command will derive information from the spec file and call a seperate (generate_source_tarball.sh) script to create a new source tarball using vendored sources. This command will also update the spec file to include the name of the new tarball and the old tarball.

    - After both command are successfully ran, there should be four items in a completed package build (generate tarball script, old source code tarball, new vendored tarball, new spec file). The User can implement this new package in their build image if they copy the directory and place it in their mariner workspace (***/CBL-Mariner/SPECS***) and update the cgmanifest (***/CBL-Mariner/cgmanifest***). 

    - Following the typical Azure Linux Build tool commands should result in a built rpm package after implementation. 

    - Additional functionality to be implemented includes a **--update** command that will recreate the vendored source tarball with updated packages if needed later in the development cycle.