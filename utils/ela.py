from PIL import Image, ImageChops, ImageEnhance
import os

def analyze_ela(image_path, quality=90):
    try:
        temp_path = image_path.replace(".", "_ela_temp.")
        ela_output_path = image_path.replace(".", "_ela.")

        original = Image.open(image_path).convert('RGB')
        original.save(temp_path, 'JPEG', quality=quality)

        compressed = Image.open(temp_path)
        diff = ImageChops.difference(original, compressed)

        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])

        if max_diff == 0:
            score = 0
            ela_image = None
        else:
            scale = 255.0 / max_diff
            diff = ImageEnhance.Brightness(diff).enhance(scale)
            diff.save(ela_output_path)
            score = min(int(max_diff * 1.5), 100)
            ela_image = os.path.basename(ela_output_path)

        os.remove(temp_path)
        return score, [f"ELA max difference: {max_diff}"], ela_image

    except Exception as e:
        return 60, [f"ELA analysis error: {str(e)}"], None
