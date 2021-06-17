from conans import ConanFile, tools

class Detours(ConanFile):
    name = "detours"
    version = "fe7216c037c898b1f65330eda85e6146b6e3cb85"
    description = "Conan recipe for Detours by Microsoft Research"
    url = "https://github.com/adamrehn/conan-recipes/detours"
    license = "MIT"
    settings = "os", "compiler", "arch"
    short_paths = True
    
    def requirements(self):
        
        # We only support building under Windows
        if self.settings.os != "Windows":
            raise RuntimeError("Only Windows is supported!")
    
    def source(self):
        
        # Clone the Detours repo and checkout our target commit
        self.run("git clone --progress https://github.com/microsoft/Detours.git detours")
        with tools.chdir("detours"):
            self.run("git checkout {}".format(self.version))
    
    def build(self):
        
        # Build Detours using nmake
        with tools.chdir("detours"):
            vcvars = tools.vcvars_command(self)
            print(vcvars)
            self.run("{} && nmake".format(vcvars))
    
    def package(self):
        
        # Detours suffixes the bin and lib directories with an architecture string
        suffix = "X64" if self.settings.arch == "x86_64" else "X86"
        
        # Copy the Detours headers and static libraries
        self.copy("*.h", dst="include", src="detours/include")
        self.copy("*.lib", dst="lib", src="detours/lib.{}".format(suffix))
        self.copy("*.pdb", dst="lib", src="detours/lib.{}".format(suffix))
        
        # Copy the Detours sample DLLs and tools
        self.copy("*.dll", dst="bin", src="detours/bin.{}".format(suffix))
        self.copy("*.exe", dst="bin", src="detours/bin.{}".format(suffix))
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
