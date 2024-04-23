import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from colorama import Fore
import warnings
from urllib3.exceptions import InsecureRequestWarning

# modifyig the code in order to ssl.1.1.1 with linux 
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


# Function to track phone number
def track_phone_number(phone_number):
    # Parse the phone number
    parsed_number = phonenumbers.parse(phone_number, None)
    
    # Get location information
    location = geocoder.description_for_number(parsed_number, "en")
    service_provider = carrier.name_for_number(parsed_number, "en")
    
    # Check if location and service provider are available
    if location:
        print("Location:", location)
    else:
        print("Location: Unknown")
    
    if service_provider:
        print("Service Provider:", service_provider)
    else:
        print("Service Provider: Unknown")

# Function to get approximate coordinates
def get_approx_coordinates(location):
    # OpenCageGeocode API key, create an account
    api_key = "ed65a92b278c4ab08c994727faade01d"
    coder = OpenCageGeocode(api_key)
    
    # Get geocoding results for the provided location
    results = coder.geocode(location)
    
    # Check if any results were obtained
    if results:
        # Extract latitude and longitude from the results
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        
        # Print latitude and longitude
        print("[+] Latitude: {}, Longitude: {}".format(latitude, longitude))
        
        # Get address information for the coordinates
        address_results = coder.reverse_geocode(latitude, longitude)
        
        # Check if any address results were obtained
        if address_results:
            # Extract the formatted address
            address = address_results[0]['formatted']
            
            # Print the approximate location
            print(Fore.LIGHTRED_EX + "[+] Approximate Location: {}".format(address))
        else:
            print(Fore.RED + "[-] No address found for the given coordinates.")
    else:
        print(Fore.RED + "[-] No results found for the given location.")

# Load the phone number from the separate file
from phone import number

# Check if phone number is available
if number:
    track_phone_number(number)
else:
    print("Error: Phone number not available.")

