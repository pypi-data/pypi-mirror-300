# tekdate/module.py


# create a fucntion that explains new format
def tekdate_description():
    description = """
    tekdate Format is a modern and human-readable way to represent date and time. It removes the ambiguity caused by 
    region-specific formats by clearly labeling each component: 'y' for year, 'm' for month, 'd' for day, 'h' for hour, 
    'm' for minute, 's' for seconds, and 'z' for time zone. The format prioritizes simplicity and clarity, making it 
    easy to read and parse by both humans and machines. TekDate supports optional time zone information and ensures 
    global consistency, reducing confusion across platforms. With no separators like slashes or colons, it’s designed 
    for efficiency and accuracy. 
    Example: y2024m03d02h20m15s205z+0530
    """
    return description
