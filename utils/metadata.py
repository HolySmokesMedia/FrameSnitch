from PIL import Image
from PIL.ExifTags import TAGS

def analyze_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        score = 0
        details = []

        if exif_data is None:
            score = 70  # No metadata? That’s sus.
            details.append("No EXIF metadata found.")
        else:
            exif_cleaned = {TAGS.get(tag): value for tag, value in exif_data.items() if tag in TAGS}

            # Check if key tags exist
            required_tags = ['DateTime', 'Make', 'Model']
            for tag in required_tags:
                if tag not in exif_cleaned:
                    score += 10
                    details.append(f"Missing {tag} tag.")

            # GPS check
            if 'GPSInfo' not in exif_cleaned:
                score += 10
                details.append("No GPS data.")

            # Limit to max score of 100
            score = min(score, 100)

        return score, details

    except Exception as e:
        return 80, [f"Metadata analysis error: {str(e)}"]
