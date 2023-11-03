import os
import httpx
import asyncio
import aiofiles
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from log.dependencies import setup_logger
logger = setup_logger(__name__)

async def save_img_from_url(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        buffer = response.content
        filename = f"{datetime.now().timestamp()}.png"
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(buffer)
        return filename
    except Exception as err:
        print(err)
        raise err

async def delete_file(filename):
    try:
        os.remove(filename)
        return "Deleted file: " + filename
    except Exception as err:
        print(err)

async def dalle_img_to_cf(url=""):
    try:
        if not url:
            raise ValueError("URL is required")
        filename = await save_img_from_url(url)
        cf_url = await upload_to_cloudflare(filename)
        await delete_file(filename)
        return cf_url
    except Exception as err:
        print(err)
        raise err

async def convert_heic(input_buffer, quality=1.0):
    try:
        print(f"Converting HEIC to JPEG with quality = {quality}")
        # Assuming a function to convert HEIC to JPEG
        output_buffer = convert_heic_to_jpeg(input_buffer, quality)  # You need to define this function
        return output_buffer
    except Exception as err:
        raise ValueError(f"Error converting HEIC to JPEG: {err}")

async def upload_to_cloudflare(filename, file=None, heic_buffer=None):
    try:
        if not file:
            async with aiofiles.open(filename, mode='rb') as f:
                blob = await f.read()
        else:
            blob = file

        quality = 0.75
        # while len(str(blob)) >= 8 and quality >= 0.25:
        #     if not heic_buffer:
        #         raise ValueError("HEIC buffer is required to convert to JPEG")
        #     print(f"File is too large to be sent to Cloudflare -- decreasing quality to {quality}")
        #     blob = await convert_heic(heic_buffer, quality)
        #     quality -= 0.25

        # if len(str(blob)) > 8:
        #     raise ValueError("File is too large to be sent to Cloudflare")

        print(f"Uploading file to cloudflare...{filename} :: {len(blob)}")

        files = {'file': (filename, blob)}
        headers = {
            'Authorization': f'Bearer {os.getenv("CF_IMAGE_KEY")}',
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.cloudflare.com/client/v4/accounts/81f991621b293527970f6b95fd1e3c52/images/v1",
                files=files,
                headers=headers,
                timeout=60
            )

            logger.debug(response)

        return extract_url(response.json())

    except httpx.HTTPError as error:
        print(error)
        raise ValueError(f"Error uploading to Cloudflare {error}")

def extract_url(input):
    try:
        print("Extracting URL from CF response")
        variants = input['result']['variants'][0]
        return variants
    except Exception as err:
        print(err)

# Dummy function to represent HEIC to JPEG conversion
# You should replace this with actual conversion logic
def convert_heic_to_jpeg(input_buffer, quality):
    # Placeholder for actual HEIC to JPEG conversion
    return input_buffer

if __name__ == "__main__":
    # Example usage
    asyncio.run(dalle_img_to_cf("https://example.com/image.png"))
