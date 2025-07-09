from utils.metadata import analyze_metadata
from utils.frequency import analyze_frequency
from utils.ela import analyze_ela

def analyze_ai_likelihood(image_path):
    metadata_score, metadata_flags = analyze_metadata(image_path)
    freq_score, freq_flags = analyze_frequency(image_path)
    ela_score, ela_flags, _ = analyze_ela(image_path)

    flags = []
    ai_score = 0

    # Check for missing EXIF data
    if "No EXIF metadata found." in metadata_flags:
        ai_score += 30
        flags.append("No EXIF metadata detected")

    if any("Missing" in f for f in metadata_flags):
        ai_score += 20
        flags.append("Missing camera info")

    if freq_score > 60:
        ai_score += 25
        flags.append("High-frequency pattern detected")

    if ela_score < 10:
        ai_score += 15
        flags.append("Low ELA difference (uniform structure)")

    ai_score = min(ai_score, 100)

    return ai_score, flags
