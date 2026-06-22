import os
from typing import List, Literal
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from io import BytesIO

# 1. Define your updated schema
class Schedule(BaseModel):
    type: Literal["as needed", "intervaled"] = Field(
        description="The type of schedule."
    )
    interval_h: int = Field(
        description="The interval in hours. Set to 0 if the type is 'as needed'."
    )
    condition: List[str] = Field(
        description="Conditions under which this schedule applies."
    )

class MedicationInfo(BaseModel):
    brand: str = Field(description="The brand name of the medication or product.")
    desc: str = Field(description="A brief description of the product.")
    uses: List[str] = Field(description="List of primary uses or indications.")
    dosage: str = Field(
        description="Descriptive dosage instructions, e.g., '3 times a day', 'as needed'."
    )
    schedule: Schedule
    warnings: List[str] = Field(
        description="List of warnings, side effects, or contraindications."
    )
    all_desc: str = Field(
        description="A single field containing all information compiled into a descriptive text form."
    )

# 2. Initialize the client
client = genai.Client(api_key="")

# 3. Load your image (replace with your actual image path)
# This can be a JPEG or PNG photo of a medical label, box, or document.


def dollm(Imagebytes):
    try:
        medication_image = Image.open(BytesIO(Imagebytes))
    except FileNotFoundError:
        print("Imagebytes cannot load")
        exit()

    # 4. Make the multimodal structured call
    prompt = """describe this medicine, do not put sources, answer in indonesia
if you cannot read teh image, return
{ error: string }"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        # Pass both the image object and your text instructions in the contents list
        contents=[medication_image, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MedicationInfo,
            temperature=0.1,
        ),
    )

    # 5. Output the structured JSON
    return response.text