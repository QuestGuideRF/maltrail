from thirdparty .odict import OrderedDict
class LRUDict (object ):
    def __init__ (self ,capacity ):
        self .capacity =capacity
        self .cache =OrderedDict ()
    def __len__ (self ):
        return len (self .cache )
    def __contains__ (self ,key ):
        return key in self .cache
    def __getitem__ (self ,key ):
        try :
            value =self .cache .pop (key )
            self .cache [key ]=value
        except :
            value =None
        return value
    def get (self ,key ):
        return self .__getitem__ (key )
    def __setitem__ (self ,key ,value ):
        try :
            self .cache .pop (key )
        except KeyError :
            if len (self .cache )>=self .capacity :
                self .cache .popitem (last =False )
        self .cache [key ]=value
    def set (self ,key ,value ):
        self .__setitem__ (key ,value )
    def keys (self ):
        return self .cache .keys ()