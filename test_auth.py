"""Quick test to diagnose ESPN authentication issues."""
import os
import requests

print("=" * 60)
print("ESPN Authentication Diagnostic Test")
print("=" * 60)

# Check if secrets exist
espn_s2 = os.getenv('ESPN_S2')
swid = os.getenv('SWID')

print("\n1. Checking if secrets are loaded:")
print(f"   ESPN_S2: {'✓ Found' if espn_s2 else '✗ NOT FOUND'}")
if espn_s2:
    print(f"   ESPN_S2 length: {len(espn_s2)} characters")
print(f"   SWID: {'✓ Found' if swid else '✗ NOT FOUND'}")
if swid:
    print(f"   SWID value: {swid}")
    print(f"   SWID length: {len(swid)} characters")

print("\n2. Common Issues to Check:")
print("   - ESPN_S2 should be 200+ characters long")
print("   - SWID should include curly brackets like {ABC123-...}")
print("   - Make sure you copied the FULL value from browser cookies")
print("   - Values should not have quotes around them in Secrets")

# Try a test request to ESPN
print("\n3. Testing connection to ESPN API:")
test_league_id = input("\nEnter your league ID to test (or press Enter to skip): ").strip()

if test_league_id:
    try:
        url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{test_league_id}"
        
        # Test without auth
        print(f"\n   Testing PUBLIC access (no cookies)...")
        response_public = requests.get(url)
        print(f"   Status: {response_public.status_code}")
        
        if espn_s2 and swid:
            # Test with auth
            print(f"\n   Testing PRIVATE access (with cookies)...")
            cookies = {'espn_s2': espn_s2, 'SWID': swid}
            response_private = requests.get(url, cookies=cookies)
            print(f"   Status: {response_private.status_code}")
            
            if response_private.status_code == 200:
                print("   ✓ Authentication successful!")
            elif response_private.status_code == 401:
                print("   ✗ Authentication failed - Invalid credentials")
                print("   Check that you copied the full cookie values correctly")
            elif response_private.status_code == 403:
                print("   ✗ Forbidden - Possible issues:")
                print("     - Cookies may have expired (login to ESPN again)")
                print("     - Not a member of this league")
                print("     - League ID is incorrect")
            else:
                print(f"   ✗ Unexpected error: {response_private.status_code}")
        else:
            print("\n   ⚠ Skipping private access test - secrets not found")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
else:
    print("   Skipped test request")

print("\n" + "=" * 60)
