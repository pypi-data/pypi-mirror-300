from collections.abc import Hashable, Iterable
from typing import Any, Optional, Tuple

class SymmetricMatrix:
    
    def __init__( self, keys:Optional[ Iterable[ Hashable ] ] = None, frozen_keys:bool = False ) -> None:
        """
        Initializes the SymmetricMatrix with optional keys and a flag to freeze keys.

        Args:
            keys (Optional[Iterable]): An iterable of keys to initialize the matrix. Defaults to None.
            frozen_keys (bool): If True, keys cannot be added after initialization. Defaults to False.
        """
        
        #TODO Handle values initializer
        self.__values: dict[ Tuple[ Hashable, Hashable ], Any ] = {}
        
        # First allows keys to be unfrozen for initialization
        self.__frozen_keys = False
        
        #The keys of the correlation matrix are stored in a set
        self.__keys: frozenset[ Hashable ] = frozenset()
        
        # Initiates all keys if provided
        if keys is not None:
            for key in keys:
                self._initiate_key( key )

        # Then, determines whether the keys should be frozen or not
        self.__frozen_keys = frozen_keys

        

    @property
    def keys( self ) -> frozenset[ Hashable ]:
        """
        Returns a copy of the keys.

        Returns:
            set: A copy of the keys of the matrix.
        """
        #We return a copy of the keys
        return self.__keys


    @staticmethod
    def _check_key_type( key ) -> bool:
        """
        Checks if the key is a 2-tuple.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key is a 2-tuple, False otherwise.
        """
        return isinstance( key, tuple ) and len( key ) == 2
        
    def __keys_exist( self, key1, key2 ) -> bool:
        """
        Checks if both keys exist in the matrix.

        Args:
            key1: The first key to check.
            key2: The second key to check.

        Returns:
            bool: True if both keys exist, False otherwise.
        """
        
        return key1 in self.__keys and key2 in self.__keys

    def _initiate_key( self, key ) -> None:
        """
        Adds a key to the matrix.

        Args:
            key: The key to add.
        """
        if self.__frozen_keys:
            raise IndexError( f"Cannot add key '{key}' becauses keys are frozen." )
        else:
            self.__keys = self.__keys | frozenset( [ key ] )


    def __getitem__( self, key_pair: tuple ) -> float:
        """
        Gets the value associated with the given key.

        Args:
            key_pair (tuple): The key for which to get the value.

        Returns:
            float: The value associated with the key.
        """
        
        if self._check_key_type( key_pair ):

            #We get the two keys requested
            key1, key2 = key_pair

            return self._get_value( key1, key2 ) #Note: we could also write self.get_value( *key )
        else:
            raise TypeError( f"Keys should be expressed as 2-tuple, provided {type(key_pair)}")

    def __setitem__( self, key_pair: tuple, value:float ) -> None:
        """
        Sets the value for the given key.

        Args:
            key_pair (tuple): The key pair for which to set the value.
            value (float): The value to set for the key.
        """

        if not isinstance( value, float ):
            raise TypeError( f"Value should be expressed as a float, provided {type(value)}")

        if not self._check_key_type( key_pair ):
            raise TypeError( f"Keys should be expressed as 2-tuple, provided {type(key_pair)}")

        key1, key2 = key_pair
        if self.__keys_exist( *key_pair ):
            #The pair already exists, we can set the value
            #We check if a value was already assigned
            the_key = self._get_values_key( key1, key2 )
            if the_key is None:
                #If not, we define the pair
                the_key = key_pair 
            
            #We assigne the value to the pair
            self.__values[ the_key ] = value 

        else:
            #Keys are not frozen, so we can add the one required

            if key1 not in self.__keys:
                self._initiate_key( key1 )

            if key2 not in self.__keys:
                self._initiate_key( key2 )

            the_key = self._get_values_key( key1, key2 )
            
            if the_key is None:
                #If this pair was never set, we use a default pair
                the_key = key_pair
            
            self.__values[ the_key ] = value 
        


    def __contains__( self, key_pair:tuple ) -> bool:
        """
        Checks if the matrix contains a value for the given key pair.

        Args:
            key_pair (tuple): The key to check.

        Returns:
            bool: True if the matrix contains a value for the key, False otherwise.
        """
        if self._check_key_type( key_pair ):
            key1, key2 = key_pair
            return self._get_values_key( key1, key2 ) is not None
        else:
            raise TypeError( f"Keys should be expressed as 2-tuple, provided {type(key_pair)}")

    def _get_values_key( self, key1, key2 ) -> Optional[ tuple ]:
        """
        Returns the key pair used for storing the value for the given key pair.

        Args:
            key1: The first key of the pair.
            key2: The second key of the pair.

        Returns:
            Optional[tuple]: The key used for storing the value, or None if not found.
        """

        if ( key1, key2 ) in self.__values:
            return ( key1, key2 )
        elif ( key2, key1 ) in self.__values:
            return ( key2, key1 )
        else:
            #We did not find the key pair
            return None

    def _get_value( self, key1, key2 ) -> float:
        """
        Returns the value associated with the given key pair.

        Args:
            key1: The first key of the pair.
            key2: The second key of the pair.

        Returns:
            float: The value associated with the key pair.
        """
        
        the_key = self._get_values_key( key1, key2 )
        if the_key is None:
            raise IndexError( f"No value for key pair : ({key1}, {key2})" )
        else:
            #We return the key from the pair
            return self.__values[ the_key ]
        
        
    def __repr__(self):
        """
        Returns a user-friendly string representation of the SymmetricMatrix instance,
        displaying the matrix in a specified format.
        """
        if not self.__keys:
            return 'Empty SymmetricMatrix'

        # Sort the keys for consistent ordering
        sorted_keys = sorted(self.__keys)
        # Gets the maximum length of the keys
        max_key_length = max(len(str(key)) for key in sorted_keys)
        # Gets the maximum length of the values
        max_value_length = max( len( str( value ) ) for value in self.__values.values() ) if len( self.__values ) > 0 else 0
        # Gets the overall maximum length
        max_length = max( max_key_length, max_value_length )

        # Create the header row
        header = ' ' * (max_key_length + 1) + ' '.join(f'{key:^{max_length}}' for key in sorted_keys)

        # Create each row of the matrix
        rows = []
        for i, key1 in enumerate(sorted_keys):
            row = [f'{key1:<{max_key_length}}']
            for j, key2 in enumerate(sorted_keys):
                if j < i:
                    # The matrix is symmmetric, no need to show one half
                    row.append(' ' * max_length)
                else:
                    try:
                        # Tries to get the value
                        value = self._get_value(key1, key2)
                    except IndexError:
                        # If value is undefined, shows ?
                        value = '?'
                    row.append(f'{value:^{max_length}}')
            rows.append(' '.join(row))

        # Combine the header and the rows into the final string
        matrix_str = '\n'.join([header] + rows)
        return matrix_str
    
    def __str__( self ) -> str:
        """
        Returns a user-friendly string representation of the SymmetricMatrix instance,
        displaying the matrix in a specified format.
        """
        
        return repr( self )
    
    def to_2d_array( self, ordered_keys: Iterable[ Hashable ]  ) ->  list[ list[ Any ] ]:
        """
        Converts the SymmetricMatrix into a 2D array.

        This method constructs a 2D array based on the values corresponding to 
        pairs of keys from `ordered_keys`. The order of the keys in `ordered_keys` 
        dictates the order of the rows and columns in the resulting 2D array.

        Parameters:
        ----------
        ordered_keys : Iterable[ Hashable ]
            An iterable (e.g., list) of keys that defines the order of rows and 
            columns in the 2D array.

        Returns:
        -------
        list[list[Any]]
            A 2D array where each element represents the value for the pair of keys 
            `(key1, key2)` based on the order defined by `ordered_keys`.

        Raises:
        -------
        TypeError
            If `ordered_keys` is not an iterable (e.g., list).

        """

        #Ensures we have one ordered set of keys
        if not isinstance( ordered_keys, Iterable ):
            raise TypeError(
                f"Invalid type for 'ordered_entities'. Expected an Iterable (e.g., list, tuple) but got "
                f"{type(ordered_keys).__name__}. Please pass a valid iterable to determine the "
                "order of rows and columns in the resulting 2D array."
            )
            
        #Builds the resulting 2d array
        result = []
        for key1 in ordered_keys:
            #Initiates row
            row = []
            for key2 in ordered_keys:
                #Adds value for pair
                row.append( self[ key1, key2 ] )
            #Adds row to final structure
            result.append( row )
            
        return result
    
    def to_2d_dict( self, selected_keys: Optional[ Iterable[ Hashable ] ] = None  ) ->  dict[ Hashable, dict[ Hashable, Any ] ]:
        """
        Converts a set of key-value pairs into a 2D dictionary.

        This method constructs a 2D dictionary where the keys from `selected_keys` 
        serve as both the row and column headers, and the values are derived 
        from the corresponding key pairs `(key1, key2)`. If `entities` is not 
        provided, the method uses `self.keys`.

        Parameters:
        ----------
        selected_keys : Optional[Iterable[Hashable]], optional
            An iterable of hashable keys that defines the order of rows and columns 
            in the 2D dictionary. If not provided, `self.keys` is used.

        Returns:
        -------
        dict[Hashable, dict[Hashable, Any]]
            A 2D dictionary where each key in the outer dictionary corresponds 
            to a row header, and each inner dictionary represents the row's 
            values with keys as column headers.

        Raises:
        -------
        TypeError
            If `selected_keys` is not an iterable (e.g., list, tuple).
        """


        #Ensures we have one ordered set of keys
        if selected_keys is None:
            selected_keys = self.keys
        elif not isinstance( selected_keys, Iterable ):
            raise TypeError(
                f"Invalid type for 'entities'. Expected an Iterable (e.g., list, tuple) but got "
                f"{type(selected_keys).__name__}. Please pass a valid iterable to determine the "
                "keys in the resulting 2D dictionary."
            )
            
        #Builds the resulting 2d dictionary
        result = {}
        for key1 in selected_keys:
            #Initiates sub-dict
            subdict = {}
            for key2 in selected_keys:
                #Adds value for pair
                subdict[ key2 ] = self[ key1, key2 ]
            #Adds subdict to final structure
            result[ key1 ] = subdict
            
        return result
    
            