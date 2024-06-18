#!/bin/bash

# Ensure the rpm file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 your-rpm-file.rpm"
    exit 1
fi

RPM_FILE=$1

# Generate the dependency list with names and versions
sudo dnf repoquery --requires --resolve --recursive --qf '%{name}-%{version}-%{release}' $RPM_FILE > dependencies.txt

# Create the DOT file
echo "digraph dependencies {" > dependencies.dot

# Initialize an associative array to track dependencies
declare -A dep_map

# Read dependencies and form the relationships
while IFS= read -r dep; do
  if [[ ! -z "$dep" ]]; then
    dep_map["$dep"]=1
  fi
done < dependencies.txt

# Output the dependencies into the DOT file
for dep in "${!dep_map[@]}"; do
  echo "\"$RPM_FILE\" -> \"$dep\";" >> dependencies.dot
done

echo "}" >> dependencies.dot

# Generate the graph image
dot -Tsvg dependencies.dot -o dependencies.svg

# Notify user
echo "Dependency graph generated as dependencies.png"