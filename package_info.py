class PackageInfo(object):
    def __init__(self, info_file):
        with open(info_file) as f:
            exec(f.read(), self.__dict__)
        self.__dict__.pop('__builtins__', None)

    def __getattribute__(self, name):
        return super(PackageInfo, self).__getattribute__(name)
