import re

async def process_with_local_model(raw_text: str):
    """
    Extracts structured data from the raw text using simple keyword matching and regex.
    This simulates a locally hosted model processing.
    """

    try:
        # Extract product name using basic regex
        product_match = re.search(r"(?i)ordered\s+(\d+)\s+([\w\s]+)", raw_text)
        if not product_match:
            raise ValueError("Could not extract product information from the input text.")

        quantity = int(product_match.group(1))
        product_name = product_match.group(2).strip()

        # Return structured data
        structured_data = {
            "product_name": product_name,
            "quantity": quantity
        }
        return structured_data

    except Exception as e:
        raise ValueError(f"Error processing text: {e}")
