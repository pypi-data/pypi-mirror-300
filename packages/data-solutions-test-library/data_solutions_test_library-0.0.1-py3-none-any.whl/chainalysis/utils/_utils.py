from chainalysis.utils import Stringify


class Utils:
    """
    This class contains util/helper functions for users
    of the SDK.

    :ivar stringify: Stringify class instance
    :vartype stringify: Stringify
    """

    def __init__(self):
        self.stringify = Stringify()
