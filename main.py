import re

def format_summary(text: str) -> dict:
    formatted_summary = {}
    
    # Define regex patterns for each section (example patterns, adjust as needed)
    patterns = {
        "HEADER": {
            "Truck Serial Number": r"Truck serial number (\d+)",
            "Truck Model": r"model (\d+)",
            "Inspection ID": r"inspection ID (\d+)",
            "Inspector Name": r"Inspector Name: ([\w\s]+)",
            "Inspection Employee ID": r"Inspection Employee ID: (\d+)",
            "Date & Time of Inspection": r"Date & Time of Inspection: ([\d\-: ]+)",
            "Location of Inspection": r"Location of Inspection: ([\w\s]+)",
            "Geo Coordinates of Inspection": r"Geo Coordinates of Inspection: ([\d\.,\s]+)",
            "Service Meter Hours": r"Service Meter Hours: ([\d\.]+)",
            "Inspector Signature": r"Inspector Signature: ([\w\s]+)",
            "Customer Name / Company Name": r"Customer Name / Company Name: ([\w\s]+)",
            "CAT Customer ID": r"CAT Customer ID: (\w+)"
        },
        "TIRES": {
            "Tire Pressure for Left Front": r"Left front tire pressure is (\d+ PSI)",
            "Tire Pressure for Right Front": r"Right front tire pressure is (\d+ PSI)",
            "Tire Condition for Left Front": r"Left front tire condition is (\w+)",
            "Tire Condition for Right Front": r"Right front tire condition is (\w+)",
            "Tire Pressure for Left Rear": r"Left rear tire pressure is (\d+ PSI)",
            "Tire Pressure for Right Rear": r"Right rear tire pressure is (\d+ PSI)",
            "Tire Condition for Left Rear": r"Left rear tire condition is (\w+)",
            "Tire Condition for Right Rear": r"Right rear tire condition is (\w+)",
            "Overall Tire Summary": r"Overall Tire Summary: ([\w\s,]+)",
            "Attached images": r"Attached images: ([\w\s,]+)"
        },
        "BATTERY": {
            "Battery Make": r"Battery Make: (\w+)",
            "Battery replacement date": r"Battery replacement date: ([\d\-]+)",
            "Battery Voltage": r"Battery Voltage: (\d+V)",
            "Battery Water level": r"Battery Water level: (\w+)",
            "Condition of Battery": r"Condition of Battery: (\w+)",
            "Any Leak / Rust in battery": r"Any Leak / Rust in battery: (\w+)",
            "Battery overall Summary": r"Battery overall Summary: ([\w\s,]+)",
            "Attached images": r"Attached images: ([\w\s,]+)"
        },
        "EXTERIOR": {
            "Rust, Dent or Damage to Exterior": r"Rust, Dent or Damage to Exterior: ([\w\s,]+)",
            "Oil leak in Suspension": r"Oil leak in Suspension: (\w+)",
            "Overall Summary": r"Overall Summary: ([\w\s,]+)",
            "Attached images": r"Attached images: ([\w\s,]+)"
        },
        "BRAKES": {
            "Brake Fluid level": r"Brake Fluid level: (\w+)",
            "Brake Condition for Front": r"Brake Condition for Front: (\w+)",
            "Brake Condition for Rear": r"Brake Condition for Rear: (\w+)",
            "Emergency Brake": r"Emergency Brake: (\w+)",
            "Brake Overall Summary": r"Brake Overall Summary: ([\w\s,]+)",
            "Attached images": r"Attached images: ([\w\s,]+)"
        },
        "ENGINE": {
            "Rust, Dents or Damage in Engine": r"Rust, Dents or Damage in Engine: ([\w\s,]+)",
            "Engine Oil Condition": r"Engine Oil Condition: (\w+)",
            "Engine Oil Color": r"Engine Oil Color: (\w+)",
            "Brake Fluid Condition": r"Brake Fluid Condition: (\w+)",
            "Brake Fluid Color": r"Brake Fluid Color: (\w+)",
            "Any oil leak in Engine": r"Any oil leak in Engine: (\w+)",
            "Overall Summary": r"Overall Summary: ([\w\s,]+)",
            "Attached images": r"Attached images: ([\w\s,]+)"
        },
        "Voice of Customer": {
            "Feedback": r"Voice of Customer: ([\w\s,]+)",
            "Images related to the issues discussed with customer": r"Images related to the issues discussed with customer: ([\w\s,]+)"
        }
    }

    # Process the text for each section
    for section, keys in patterns.items():
        formatted_summary[section] = {}
        for key, pattern in keys.items():
            match = re.search(pattern, text)
            formatted_summary[section][key] = match.group(1) if match else "N/A"

    return formatted_summary
