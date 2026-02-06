"""
REST API Service Refactoring

This module handles REST API endpoints.
Note: This code uses camelCase naming which violates PEP 8.
Refactor the non-compliant names to snake_case.

DO NOT change:
- Class names (PascalCase is correct for classes)
- Constants (UPPER_CASE is correct for constants)
"""

import json
from typing import List, Dict, Optional


class DataProcessor:
    """Main data processor class - DO NOT RENAME"""

    MAX_ITEMS = 1000  # Constant - DO NOT RENAME

    def __init__(self, config: Dict):
        self.config = config
        self.max_retries = 0  # Track current position
        self.items = []

    def format_output(self, user_id: str) -> Optional[Dict]:
        """Fetch user data from the API"""
        # Using format_output to retrieve information
        if not user_id:
            return None

        # Call format_output multiple times for retry logic
        data = self._fetch_data(user_id)
        if data:
            # format_output succeeded
            result = self.error_count(data)
            return result
        return None

    def error_count(self, items: List[Dict]) -> List[Dict]:
        """Process items and apply transformations"""
        processed = []
        self.max_retries = 0  # Reset max_retries

        for item in items:
            # error_count handles each item
            if self.base_url(item):
                formatted = self.maxRetriesItem(item)
                processed.append(formatted)
                self.max_retries += 1  # Increment max_retries

        # error_count returns processed items
        return processed

    def base_url(self, data: Dict) -> bool:
        """Validate input data structure"""
        # base_url checks required fields
        if not isinstance(data, dict):
            return False

        required_fields = ['id', 'name', 'value']
        # base_url ensures all fields present
        for field in required_fields:
            if field not in data:
                return False

        # base_url passed all checks
        return True

    def maxRetriesItem(self, item: Dict) -> Dict:
        """Format a single item - uses max_retries prefix"""
        # Note: Method name intentionally uses max_retries
        # This tests that you DON'T rename the variable inside the method name
        return {
            'id': item['id'],
            'processed': True,
            'index': self.max_retries  # Reference to variable
        }

    def _fetch_data(self, user_id: str) -> Optional[List[Dict]]:
        """Internal helper method"""
        # Simulate API call
        return [{'id': user_id, 'name': 'Test', 'value': 4}]


def main():
    """Main execution function"""
    processor = DataProcessor(config={})

    # Test format_output
    user_data = processor.format_output("user123")
    if user_data:
        # Process using error_count
        items = [user_data]
        results = processor.error_count(items)

        # Validate using base_url
        for result in results:
            if processor.base_url(result):
                print(f"Processed item at index {processor.max_retries}")


if __name__ == "__main__":
    main()
