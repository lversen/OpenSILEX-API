#!/usr/bin/env python3
"""
Final test after applying all fixes
"""

print("OpenSILEX Client Authentication Test")
print("=" * 50)

# Test 1: Import and initialize
try:
    from client import OpenSilexClient
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    exit(1)

# Test 2: Create client
try:
    client = OpenSilexClient("http://20.4.208.154:28081/rest")
    print("✓ Client created")
except Exception as e:
    print(f"✗ Client creation error: {e}")
    exit(1)

# Test 3: Authenticate
try:
    print("\nAuthenticating...")
    auth_response = client.authenticate("admin@opensilex.org", "admin")
    
    print(f"Auth response success: {auth_response.success}")
    print(f"Auth response data: {auth_response.data}")
    
    if auth_response.success:
        print("✓ Authentication successful!")
        
        # Test 4: Make authenticated request
        print("\nTesting authenticated request...")
        system_info = client.get_system_info()
        
        if system_info.success:
            print("✓ System info retrieved successfully!")
            print(f"  Version info: {system_info.data}")
        else:
            print(f"✗ Failed to get system info: {system_info.errors}")
    else:
        print(f"✗ Authentication failed!")
        print(f"  Message: {auth_response.message}")
        print(f"  Errors: {auth_response.errors}")
        
except Exception as e:
    print(f"✗ Error during authentication: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Cleanup
try:
    if client.is_authenticated():
        logout_response = client.logout()
        print(f"\n✓ Logged out: {logout_response.success}")
except:
    pass

print("\n" + "=" * 50)
print("Test complete!")