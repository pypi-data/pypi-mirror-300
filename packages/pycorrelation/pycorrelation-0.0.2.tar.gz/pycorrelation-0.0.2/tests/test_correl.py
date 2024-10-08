import pytest
from src.pycorrelation.symmetric_matrix import SymmetricMatrix
from src.pycorrelation.correl import CorrelationMatrix


def build_sample_matrix():
    """Builds sample matrix"""
    
    
    matrix = SymmetricMatrix()
    matrix[ 'a', 'a' ] = 0.09
    matrix[ 'a', 'b' ] = 0.9
    matrix[ 'b', 'b' ] = 0.08
    matrix[ 'a', 'c' ] = 0.7
    matrix[ 'b', 'c' ] = 0.6
    matrix[ 'c', 'c' ] = 0.06
    
    return matrix


def symmetric_assignment( matrix, key1, key2, value ):
    matrix[ key1, key2 ] = value
    assert matrix[ key1, key2 ] == value
    # Test if the matrix is symmetric
    assert matrix[ key2, key1 ] == value

    

    

def test_initialization():
    # Test if the matrix is initialized with the correct keys
    matrix = SymmetricMatrix(keys=['a', 'b', 'c'])
    assert set(matrix.keys) == {'a', 'b', 'c'}

def test_symmetric_assignment_SM():
    # Test setting and getting an item in the matrix
    matrix = SymmetricMatrix()
    symmetric_assignment( matrix, 'a', 'b', 0.5 )

def test_symmetric_assignment_CM():
    # Test setting and getting an item in the matrix
    matrix = CorrelationMatrix()
    symmetric_assignment( matrix, 'a', 'b', 0.5 )


def test_set_and_get_item_initialized():
    # Test setting and getting an item in the matrix
    matrix = SymmetricMatrix(keys=['a','b'])
    #The value is not yet set
    assert ('a','b') not in matrix
    assert ('b','a') not in matrix
    assert ('a','a') not in matrix
    assert ('b','b') not in matrix
    
    #We set the value
    symmetric_assignment( matrix, 'a', 'b', 0.5 )
    
    #The value is now set
    assert ('a','b') in matrix
    assert ('b','a') in matrix
    #But still not the diagonal
    assert ('a','a') not in matrix
    assert ('b','b') not in matrix
    
    
    symmetric_assignment( matrix, 'a', 'a', 0.2 )
    assert ('a','a') in matrix
    
    symmetric_assignment( matrix, 'b', 'b', -0.33 )
    assert ('b','b') in matrix
    
    
    

def test_key_error():
    # Test if an IndexError is raised when trying to access a non-existent key
    matrix = SymmetricMatrix()
    with pytest.raises(IndexError):
        matrix['a', 'b']

def test_key_type_error():
    # Test if a TypeError is raised when the key is not a 2-tuple
    matrix = SymmetricMatrix()
    with pytest.raises(TypeError):
        matrix['a'] = 0.5
    with pytest.raises(TypeError):
        matrix[('a', 'b', 'c')] = 0.5

def test_value_type_error():
    # Test if a TypeError is raised when the value is not a float
    matrix = SymmetricMatrix()
    with pytest.raises(TypeError):
        matrix['a', 'b'] = 'not a float'
        

def test_frozen_keys():
    # Test if keys are frozen and cannot be added after initialization
    matrix = SymmetricMatrix(keys=['a', 'b'], frozen_keys=True)
    with pytest.raises(IndexError):
        matrix['a', 'c'] = 0.5
    assert 'a' in matrix.keys
    assert 'c' not in matrix.keys

def test_contains():
    # Test if the __contains__ method works correctly
    matrix = SymmetricMatrix()
    matrix['a', 'b'] = 0.5
    assert ('a', 'b') in matrix
    assert ('b', 'a') in matrix
    assert ('a', 'c') not in matrix


def test_2d_array_wrong_type():
    #Tests whether 2d array requires a list
    
    matrix = build_sample_matrix()
    
    with pytest.raises(TypeError):
        array_result = matrix.to_2d_array( 12.4 )
    
    
def test_2d_array():
    #Tests whether 2d array requires a list
    
    matrix = build_sample_matrix()
    
    
    array_result = matrix.to_2d_array( [ 'b','c','a' ] )
    
    assert array_result[ 0 ][ 0 ] == matrix['b','b']


def test_2d_dict():
    #Tests whether 2d array requires a list
    
    matrix = build_sample_matrix()
    
    
    dict_result = matrix.to_2d_dict()
    
    for k1 in matrix.keys:
        for k2 in matrix.keys:
            assert matrix[ k1, k2 ] == dict_result[ k1 ][ k2 ]



##############################
# Correlation Specific Tests #
##############################

def test_correl_auto_assign():

    rho = CorrelationMatrix( [ 'a', 'b', 'c' ] )
    assert rho[ 'a', 'a' ] == 1.0
    assert rho[ 'b', 'b' ] == 1.0
    assert rho[ 'c', 'c' ] == 1.0
    


def test_non_existing_same_key():

    rho = CorrelationMatrix()
    with pytest.raises( IndexError ):
        #Should not be allowd
        x = rho[ "A", "A" ]
    
    #Should work 
    rho[ "A", "A" ] = 1.0
    
    val = rho[ "A", "A" ]
    assert val == 1.0
    
def test_existing_same_key():

    rho = CorrelationMatrix(keys=['a','b'])
    
    assert ('a', 'a') in rho
    assert ('b', 'b') in rho
    assert ('a', 'b') not in rho
    

def test_set_key_pair_invalid_value():
    """Ensure correlation matrices cannot have values > 1 or < -1"""
    rho = CorrelationMatrix()
    
    with pytest.raises( ValueError ):
        rho[ "A", "B" ] = 1.1
        
    with pytest.raises( ValueError ):
        rho[ "A", "B" ] = -1.1