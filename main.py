import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi.responses import StreamingResponse

# Apply nest_asyncio
nest_asyncio.apply()

# Define the model
model = genai.GenerativeModel('models/gemini-pro')

# Define the inspection template format
INSPECTION_TEMPLATE_FORMAT = '''
HEADER
▪ Truck Serial Number
▪ Truck Model
▪ Inspection ID
▪ Inspector Name
▪ Inspection Employee ID
▪ Date & Time of Inspection
▪ Location of Inspection
▪ Geo Coordinates of Inspection (optional, in case of remote location)
▪ Service Meter Hours (Odometer reading)
▪ Inspector Signature
▪ Customer Name / Company name
▪ CAT Customer ID

TIRES
▪ Tire Pressure for Left Front
▪ Tire Pressure for Right Front
▪ Tire Condition for Left Front
▪ Tire Condition for Right Front
▪ Tire Pressure for Left Rear
▪ Tire Pressure for Right Rear
▪ Tire Condition for Left Rear
▪ Tire Condition for Right Rear
▪ Overall Tire Summary
▪ Attached images of each tire in the same order.

BATTERY
▪ Battery Make
▪ Battery replacement date
▪ Battery Voltage
▪ Battery Water level
▪ Condition of Battery
▪ Any Leak / Rust in battery
▪ Battery overall Summary
▪ Attached images

EXTERIOR
▪ Rust, Dent or Damage to Exterior
▪ Oil leak in Suspension
▪ Overall Summary
▪ Attached images

BRAKES
▪ Brake Fluid level
▪ Brake Condition for Front
▪ Brake Condition for Rear
▪ Emergency Brake
▪ Brake Overall Summary
▪ Attached images

ENGINE
▪ Rust, Dents or Damage in Engine
▪ Engine Oil Condition
▪ Engine Oil Color
▪ Brake Fluid Condition
▪ Brake Fluid Color
▪ Any oil leak in Engine
▪ Overall Summary
▪ Attached images

Voice of Customer
▪ Any feedback from Customer
▪ Images related to the issues discussed with customer.
'''

app = FastAPI()

# Define the request model
class TextRequest(BaseModel):
    text: str

# Define the response model for categorizing text
class CategorizedResponse(BaseModel):
    result: str

# Define the response model for formatting summary
class FormattedResponse(BaseModel):
    formatted_summary: dict

# Function to format the inspection report
def format_summary(text: str) -> dict:
    # Basic implementation of formatting; replace with your own logic
    return {
        "HEADER": {
            "Truck Serial Number": "73592849",
            "Truck Model": "730",
            "Inspection ID": "002",
            "Inspector Name": "John Doe",
            "Inspection Employee ID": "12345",
            "Date & Time of Inspection": "2024-08-10 10:00 AM",
            "Location of Inspection": "Site A",
            "Geo Coordinates of Inspection": "37.7749 N, 122.4194 W",
            "Service Meter Hours": "1234.5",
            "Inspector Signature": "John Doe",
            "Customer Name / Company Name": "Acme Corp",
            "CAT Customer ID": "ACME1234"
        },
        "TIRES": {
            "Left Front Pressure": "28 PSI",
            "Right Front Condition": "Needs Replacement",
            "Left Rear Condition": "Good",
            "Right Rear Condition": "Okay",
            "Overall Tire Summary": "The tires are in mixed condition. Immediate attention needed for right front tire."
        },
        "BATTERY": {
            "Battery Make": "CAT",
            "Battery replacement date": "2024-07-15",
            "Battery Voltage": "12V",
            "Battery Water level": "Low",
            "Condition of Battery": "Rust present",
            "Any Leak / Rust in battery": "Yes",
            "Battery overall Summary": "Battery shows signs of rust and low water level. Consider replacement.",
        },
        "EXTERIOR": {
            "Rust, Dent or Damage to Exterior": "Dent on the left side, rust on suspension",
            "Oil leak in Suspension": "Yes",
            "Overall Summary": "Exterior has visible damage and rust.",
        },
        "BRAKES": {
            "Brake Fluid level": "Okay",
            "Brake Condition for Front": "Needs Replacement",
            "Brake Condition for Rear": "Okay",
            "Emergency Brake": "Good",
            "Brake Overall Summary": "Brakes need immediate attention for the front.",
        },
        "ENGINE": {
            "Rust, Dents or Damage in Engine": "Rust present",
            "Engine Oil Condition": "Good",
            "Engine Oil Color": "Brown",
            "Brake Fluid Condition": "Good",
            "Brake Fluid Color": "Clean",
            "Any oil leak in Engine": "No",
            "Overall Summary": "Engine oil is brown but in good condition. Some rust present.",
        },
        "Voice of Customer": {
            "Feedback": "Satisfied with the service but concerned about the rust on the engine and battery."
        }
    }

# Endpoint to categorize text
@app.post("/categorize", response_model=CategorizedResponse)
async def categorize_text(request: TextRequest):
    prompt = f"{INSPECTION_TEMPLATE_FORMAT}. Text: {request.text}"
    try:
        result = model.generate_content(prompt)
        return CategorizedResponse(result=result.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to format summary
@app.post("/format-summary", response_model=FormattedResponse)
async def format_summary_endpoint(request: TextRequest):
    try:
        formatted = format_summary(request.text)
        return FormattedResponse(formatted_summary=formatted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to generate PDF report
@app.post("/generate-pdf")
async def generate_pdf(request: TextRequest):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Header
        c.drawString(100, height - 50, "Inspection Report")
        c.drawString(100, height - 70, f"Truck Serial Number: {request.text['Truck Serial Number']}")
        c.drawString(100, height - 90, f"Truck Model: {request.text['Truck Model']}")
        c.drawString(100, height - 110, f"Inspection ID: {request.text['Inspection ID']}")
        c.drawString(100, height - 130, f"Inspector Name: {request.text['Inspector Name']}")
        c.drawString(100, height - 150, f"Date & Time of Inspection: {request.text['Date & Time of Inspection']}")
        c.drawString(100, height - 170, f"Location of Inspection: {request.text['Location of Inspection']}")
        c.drawString(100, height - 190, f"Service Meter Hours: {request.text['Service Meter Hours']}")
        c.drawString(100, height - 210, f"Customer Name / Company Name: {request.text['Customer Name / Company Name']}")
        
        # Placeholder for formatting other sections of the inspection report
        y = height - 250
        for key, value in request.text.items():
            c.drawString(100, y, f"{key}: {value}")
            y -= 20
        
        c.save()
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=inspection_report.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
