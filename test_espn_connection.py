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
print(f"Testing access to league {league_id}...")

# Test connection
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{league_id}"
cookies = {'espn_s2': espn_s2, 'SWID': swid}

try:
    response = requests.get(url, cookies=cookies)
    print(f"\nHTTP Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ SUCCESS! Authentication working correctly!")
        data = response.json()
        if 'settings' in data:
            print(f"  League Name: {data['settings'].get('name', 'N/A')}")
        print("\nYour scraper should work fine. Try running:")
        print(f"  python espn_ff_scraper.py --league_id {league_id} --years 2024")
    elif response.status_code == 401:
        print("✗ AUTHENTICATION FAILED (401 Unauthorized)")
        print("\nPossible fixes:")
        print("1. Your cookies may have expired - log into ESPN again and get fresh cookies")
        print("2. Double-check you copied the FULL espn_s2 value (should be 200+ chars)")
        print("3. Make sure SWID includes the curly brackets")
    elif response.status_code == 403:
        print("✗ FORBIDDEN (403)")
        print("\nPossible issues:")
        print("1. Cookies expired - log into ESPN and get fresh cookies")
        print("2. You're not a member of this league")
        print("3. League ID is incorrect")
    elif response.status_code == 404:
        print("✗ LEAGUE NOT FOUND (404)")
        print(f"\nLeague ID {league_id} doesn't exist or is invalid")
        print("Check your league URL: https://fantasy.espn.com/football/league?leagueId=YOUR_ID")
    else:
        print(f"✗ Unexpected response: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)
