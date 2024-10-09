# Define the name of the installer and the output file
OutFile "smallexe64_installer.exe"

# Define the installation directory (default is Program Files)
InstallDir "$PROGRAMFILES\SmallApp"

# Page for the installation
Page directory
Page instfiles

# Section that contains the installation logic
Section

  # Create the installation directory
  CreateDirectory "$INSTDIR"

  # Copy the file to the installation directory
  SetOutPath "$INSTDIR"
  File "smallexe64.exe"

SectionEnd