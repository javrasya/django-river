__author__ = 'ahmetdal'


class RiverException(Exception):
    code = None

    def __init__(self, error_code, *args, **kwargs):
        super(RiverException, self).__init__(*args, **kwargs)
        self.code = error_code
