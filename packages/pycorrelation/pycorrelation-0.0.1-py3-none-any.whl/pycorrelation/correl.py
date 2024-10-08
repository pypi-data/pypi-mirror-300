from .symmetric_matrix import SymmetricMatrix

class CorrelationMatrix( SymmetricMatrix ):
    
    def __init__( self, keys = None, frozen_keys = False ):
        
        super().__init__( keys, frozen_keys )


    def __setitem__( self, key, value:float ) -> None:

        if not self._check_key_type( key ):
            raise TypeError( f"Correlation keys should be expressed as 2-tuple, provided {type(key)}")
        else:
            key1, key2 = key
            if key1 == key2 and value != 1:
                raise ValueError( "Correlation between an two identical keys should only be 1" )
            else:
                if -1.0 <= value <= 1.0:
                    super().__setitem__( key, value )
                else:
                    raise ValueError( f"Correlation has to be in [-1,+1], provided {value}" )


    def _initiate_key(self, key) -> None:
        # Applies the logic of the super class
        super()._initiate_key(key)
        # Then, ensures that the correlation is 1
        self[ key, key ] = 1.0


    def __contains__(self, key_pair: tuple) -> bool:
        
        if not self._check_key_type( key_pair ):
            raise TypeError( f"Correlation keys should be expressed as 2-tuple, provided {type(key_pair)}")
        else:
            key1, key2 = key_pair
            if key1 == key2 and key1 in self.keys:
                return True
            else:
                return super().__contains__(key_pair)
