import os  # For directory and path functions


class FileSet:
    def __init__(self, filename, ext):
        self.target_ext = "." + ext
        (self.fname, self.ext) = ("test", "")  # default
        if filename:
            (self.fname, self.ext) = os.path.splitext(filename)

        # Determine if a file or directory was supplied
        self.type_file = False
        self.type_dir = False
        if self.ext:
            if self.ext == self.target_ext:
                self.type_file = True
        else:
            self.type_dir = True

        self.fileList = []
        self.dirList = []

        # Supplied name is a file of the correct extension
        if self.type_file:
            if os.path.isfile(filename):
                self.dirList = [filename]

        # Supplied name is a directory
        if self.type_dir:
            if os.path.isdir(self.fname):
                self.dirList = os.listdir(self.fname)
        for filename in self.dirList:
            if os.path.splitext(filename)[1] == self.target_ext:
                if self.type_dir:
                    filename = os.path.join(self.fname, filename)
                self.fileList.append(filename)

    def report(self):
        if self.type_file:
            print("Processing FILE: %s" % self.fname)
        if self.type_dir:
            print("Processing DIRECTORY: %s" % self.fname)
        print("Files: %i" % len(self.fileList))
        for filename in self.fileList:
            print("  %s" % os.path.basename(filename))

    def has_more_files(self):
        if self.fileList:
            return True
        return False

    def next_file(self):
        filename = None
        if self.fileList:
            filename = self.fileList[0]
            self.fileList.remove(filename)
        return filename

    def basename(self):
        return self.fname
