# **tekdate** Format

Yes, I am done with ISO date format. thats why i come up the new format.

**tekdate** is a new date and time format designed for clarity and consistency across platforms.
Each component of the date and time is explicitly labeled to remove any ambiguity, making it easier to read and process.
It supports optional timezone information and can be used across programming languages and systems.

## Why this format?

We don’t need colons, slashes, or other date separators because they can sometimes make it difficult to distinguish between the day and month, and we might not always be sure which format is being used. This often depends on the country or format settings in software like Excel. This format is designed to be more human-readable, avoiding confusion while still adhering to common standards. The reason I didn’t use capital letters is to emphasize the date itself, making it easier for the eye to distinguish between numbers and letters.

## tekdate Format Structure

### Components:

- `yYYYY`: Year (e.g., `y2024` for the year 2024)
- `mMM`: Month (e.g., `m03` for March)
- `dDD`: Day (e.g., `d02` for the 2nd day)
- `hHH`: Hour in 24-hour format (e.g., `h20` for 8 PM)
- `mMM`: Minute (e.g., `m15` for 15 minutes)
- `sSSS`: Seconds and milliseconds (e.g., `s205` for 205 milliseconds)
- `z±ZZZZ` (Optional): Timezone offset from UTC (e.g., `z+0530` for Indian Standard Time)

### Example with Timezone:

-> y2024m10d04h13m59s000z+0000

## Key Features

- **Clarity**: Every part of the date and time is explicitly labeled (year, month, day, etc.).
- **Time Zone Support**: Optional timezone component (`z±ZZZZ`), or omit it for local/unspecified time.
- **Consistency**: WIll Work across platforms and programming languages(Soon).
- **Machine-Readable**: Predictable structure that is easy to parse and generate programmatically.

## Clear and Distinguishable Date Format for Simplified Handling

The custom date format y2024m10d04h13m59s000z+0000 is designed to prevent confusion and improve human readability. By clearly labeling each date and time component (e.g., "y" for year, "m" for minute), it ensures that the format is immediately understandable and eliminates ambiguity. This structure makes it easy to distinguish between different elements without relying on traditional delimiters like dashes or colons, simplifying parsing for both humans and systems. Additionally, concerns over storage efficiency are minimal given modern capacities, so the focus on clarity and ease of interpretation offers a more practical approach. This format is highly intuitive and ready for use in any context where both accuracy and simplicity are prioritized.

## Installation

...
pip install tekdate

### Python Installation

...

### Node installation

...
