import json
import webbrowser
from urllib.parse import quote


# ==========================================
# 1. TAKE INPUT FROM USER
# ==========================================

source = input("Enter source location: ").strip()

destination = input("Enter destination location: ").strip()


# ==========================================
# 2. VALIDATE INPUT
# ==========================================

if not source or not destination:

    print("\nError: Source and destination cannot be empty.")

    exit()


# ==========================================
# 3. CREATE JSON DATA
# ==========================================

data = {
    "source": source,
    "destination": destination
}


# ==========================================
# 4. CONVERT DATA INTO JSON
# ==========================================

json_data = json.dumps(
    data,
    indent=4
)


print("\n========== JSON DATA ==========")

print(json_data)


# ==========================================
# 5. READ DATA FROM JSON
# ==========================================

data = json.loads(json_data)

source = data["source"]

destination = data["destination"]


# ==========================================
# 6. CREATE GOOGLE MAPS URL
# ==========================================

url = (
    "https://www.google.com/maps/dir/?api=1"
    f"&origin={quote(source)}"
    f"&destination={quote(destination)}"
)


# ==========================================
# 7. DISPLAY URL
# ==========================================

print("\n========== GOOGLE MAPS URL ==========")

print(url)


# ==========================================
# 8. OPEN GOOGLE MAPS
# ==========================================

print("\nOpening Google Maps...")

success = webbrowser.open(url)


if success:

    print("Google Maps opened successfully!")

else:

    print("Unable to open the browser.")


# ==========================================
# 9. PROGRAM COMPLETED
# ==========================================

print("\nNavigation request completed!")
