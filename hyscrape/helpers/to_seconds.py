def to_seconds(timestring):
    """
    Converts a swimming time string to seconds.

    Handles times in the format MM:SS.hundredths or SS.hundredths.
    Also handles empty strings.

    Args:
        timestring: The swimming time string.

    Returns:
        The time in seconds as a float, or None if the input is invalid.
    """
    if not timestring:  # Handle empty string
        return 0.0  # Or None, or raise an exception, depending on your needs

    try:
        parts = timestring.split(":")
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = float(parts[1])
            total_seconds = (minutes * 60) + seconds
        elif len(parts) == 1:
            total_seconds = float(parts[0])
        else:
            return None  # Invalid format
        return total_seconds
    except ValueError:
        return None  # Handle cases where conversion to float/int fails
