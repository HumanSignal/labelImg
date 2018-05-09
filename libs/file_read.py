def read(filename, default=None):
    '''
    Read a file into a byte array
    '''
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except:
        return default
