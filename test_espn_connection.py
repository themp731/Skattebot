"""Test ESPN connection with your credentials."""
import os
import sys
import requests

espn_s2 = os.getenv('ESPN_S2')
swid = os.getenv('SWID')

if not espn_s2 or not swid:
    print("ERROR: ESPN_S2 or SWID secrets not found!")
    sys.exit(1)

print("✓ Secrets loaded successfully")
print(f"  ESPN_S2: {len(espn_s2)} characters")
print(f"  SWID: {swid}\n")

# Ask user for league ID via command line argument
if len(sys.argv) < 2:
    print("Usage: python test_espn_connection.py YOUR_LEAGUE_ID")
    print("Example: python test_espn_connection.py 123456")
    sys.exit(1)

league_id = sys.argv[1]
print(f"Testing access to league {league_id}...\n")

# Test connection with proper headers
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{league_id}"
cookies = {'espn_s2': espn_s2, 'SWID': swid}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}

try:
    # First test without cookies (public access)
    print("Test 1: Public access (no authentication)")
    response_public = requests.get(url, headers=headers)
    print(f"  Status: {response_public.status_code}")
    if response_public.status_code == 200:
        print("  ✓ This is a PUBLIC league - no authentication needed!\n")
    else:
        print(f"  This is a private league - authentication required\n")
    
    # Test with cookies (private access)
    print("Test 2: Private access (with authentication)")
    response = requests.get(url, cookies=cookies, headers=headers)
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        print("  ✓ SUCCESS! Authentication working correctly!")
        data = response.json()
        if 'settings' in data:
            print(f"\n  League Name: {data['settings'].get('name', 'N/A')}")
        print("\n✓ Your scraper should work fine. Try running:")
        print(f"  python espn_ff_scraper.py --league_id {league_id} --years 2024")
    elif response.status_code == 401:
        print("  ✗ AUTHENTICATION FAILED (401 Unauthorized)")
        print("\n  Possible fixes:")
        print("  1. Your cookies may have expired - log into ESPN again")
        print("  2. Double-check you copied the FULL espn_s2 value")
        print("  3. Make sure SWID includes the curly brackets")
    elif response.status_code == 403:
        print("  ✗ FORBIDDEN (403)")
        print("\n  Common causes:")
        print("  1. Cookies are from a DIFFERENT ESPN account")
        print("     → Make sure you're logged into the account that's in this league")
        print("  2. Cookies expired - get fresh ones")
        print("  3. You're not a member of league 149388")
        print("\n  Try this:")
        print("  1. Log OUT of ESPN completely")
        print("  2. Log back in with the account that's in the league")
        print("  3. Navigate to the league page")
        print("  4. Get fresh espn_s2 and SWID cookies")
        print("  5. Update both secrets in Replit")
    elif response.status_code == 404:
        print("  ✗ LEAGUE NOT FOUND (404)")
        print(f"\n  League ID {league_id} doesn't exist")
    else:
        print(f"  ✗ Unexpected response: {response.status_code}")
        print(f"  Response preview: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)
