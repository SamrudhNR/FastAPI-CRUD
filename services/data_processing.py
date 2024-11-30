from services.openap_service import process_with_openai
from services.local_modelservice import process_with_local_model

async def process_data_pipeline(raw_text: str, use_local_model: bool = False):
    if use_local_model:
        return await process_with_local_model(raw_text)
    else:
        return await process_with_openai(raw_text)
