import phonenumbers
import sys
import folium
import os
import argparse
from colorama import init, Fore
from phonenumbers import geocoder, timezone, carrier

init()

def get_approx_coordinates(location):
    try:

        from opencage.geocoder import OpenCageGeocode

        coder = OpenCageGeocode("ed65a92b278c4ab08c994727faade01d")

        results = coder.geocode(location)

        if results:
            latitude = results[0]['geometry']['lat']
            longitude = results[0]['geometry']['lng']
            return latitude, longitude
        else:
            print(f"{Fore.RED}[-] Error: Could not get coordinates for the location.")
            return None, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        return None, None

def process_number(number):
    
    parsed_number = phonenumbers.parse(number)

    if parsed_number:
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        print(f"{Fore.GREEN}[+] Attempting to track location of {international_format}..")
    else:
        print(f"{Fore.RED}[-] Error: Invalid phone number format.")
        return

    time_zones = timezone.time_zones_for_number(parsed_number)
    if time_zones:
        print(f"{Fore.GREEN}[+] Time Zone ID: {time_zones}")
    else:
        print(f"{Fore.RED}[-] Time Zone ID not available.")

    location = geocoder.description_for_number(parsed_number, "en")
    if location:
        print(f"{Fore.GREEN}[+] Region: {location}")
        
        latitude, longitude = get_approx_coordinates(location)
        if latitude is not None and longitude is not None:
            print(f"{Fore.GREEN}[+] Latitude: {latitude}, Longitude: {longitude}")
        else:
            print(f"{Fore.RED}[-] Error: Could not get coordinates for the location.")
    else:
        print(f"{Fore.RED}[-] Region: Unknown")

    service_provider = carrier.name_for_number(parsed_number, 'en')
    if service_provider:
        print(f"{Fore.GREEN}[+] Service Provider: {service_provider}")
    else:
        print(f"{Fore.RED}[-] Service Provider not available.")

def draw_map(latitude, longitude, location, phone_number):
    try:
        
        my_map = folium.Map(location=[latitude, longitude], zoom_start=9) #Centered map

        folium.Marker([latitude, longitude], popup=location).add_to(my_map) #Marker
        
        cleaned_phone_number = clean_phone_number(phone_number)
        file_name = f"{cleaned_phone_number}.html"

        my_map.save(file_name)

        print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")

    except NameError as e:
        print(f"{Fore.RED}[-] Error: {e}")
        sys.exit()

def clean_phone_number(phone_number):
    
    cleaned = ''.join(char for part in phone_number for char in part if char.isdigit() or char == '+')
    return cleaned or "unknown"

def cli_argument():
    try:
        
        parser = argparse.ArgumentParser(description="Get approximate location of a Phone number.")

        
        parser.add_argument("-p", "--phone", dest="phone_number", type=str,
                            help="Phone number to track. Please include the country code when specifying the number.",
                            required=True) #Command line

        argument = parser.parse_args()

        return argument

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        sys.exit()

if __name__ == "__main__":
    args = cli_argument()
    process_number(args.phone_number)
    location = geocoder.description_for_number(phonenumbers.parse(args.phone_number), "en")
    latitude, longitude = get_approx_coordinates(location)
    draw_map(latitude, longitude, location, args.phone_number)

