def test_example():
    """Simple test to verify pipeline works"""
    assert 1 + 1 == 2
    
def test_string_operations():
    """Test string operations"""
    assert "hello".upper() == "HELLO"
    
def test_list_operations():
    """Test list operations"""
    my_list = [1, 2, 3]
    assert len(my_list) == 3
    assert 1 in my_list