"""
Utility functions for data processing
"""

def load_data():
    """Load the sensor readings data"""
    return [238,128,201,175,81,287,88,141,206,263,37,237,160,257,278,193,282,182,102,264]

def process_above_threshold(items, threshold):
    """
    Process items that are above the given threshold.

    Args:
        items: List of numeric values
        threshold: Minimum value to include

    Returns:
        Dictionary with count, total, and average
    """
    count = 0
    total = 0

    for i in range(len(items)):
        if items[i] >= threshold:
            count += 1
            total += items[i]

    average = round(total / count, 2) if count > 0 else 0.0

    return {
        'count': count,
        'total': total,
        'average': f"{average:.2f}"
    }
