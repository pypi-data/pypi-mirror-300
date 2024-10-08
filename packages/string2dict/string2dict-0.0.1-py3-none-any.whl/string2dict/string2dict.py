import re
import ast
import json
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter and set it for the console handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


class String2Dict:

    def __init__(self, debug=False, logger=False):
        self.debug=debug
        self.logger = logger if logger is not None else logging.getLogger(__name__)

    def strip_surrounding_whitespace(self, string: str) -> str:

        stripped = string.strip()
        if self.debug:
            logger.debug(f"After stripping whitespace: {repr(stripped)}")
        return stripped


    def remove_embedded_markers(self, string: str) -> str:

        markers_removed = re.sub(r'```json', '', string)
        markers_removed = re.sub(r'```', '', markers_removed)
        if self.debug:
             logger.debug(f"After removing embedded markers: {repr(markers_removed)}")
        return markers_removed


    def ensure_string_starts_and_ends_with_braces(self, string: str) -> str:

        string = re.sub(r'^.*?{', '{', string, flags=re.DOTALL)
        string = re.sub(r'}.*?$', '}', string, flags=re.DOTALL)
        if self.debug:
                logger.debug(f"After ensuring braces: {repr(string)}")
        return string


    def parse_as_json(self,string: str) -> dict:

        parsed = json.loads(string)
        if self.debug:
            logger.debug("Parsed with json.loads successfully.")
        return parsed


    def parse_with_literal_eval(self,string: str) -> dict:

        parsed = ast.literal_eval(string)
        if self.debug:
                logger.debug("Parsed with ast.literal_eval successfully.")
        return parsed


    def run(self,string: str) -> dict:


        logger.debug(f"input to s2d: {repr(string)}")

        if not string:
            logger.debug("Input string is empty.")
            return None

        # Step 1: Strip surrounding whitespace
        string = self.strip_surrounding_whitespace(string)

        # Step 2: Remove embedded markers
        string = self.remove_embedded_markers(string)

        # Step 3: Ensure the string starts and ends with braces
        string = self.ensure_string_starts_and_ends_with_braces(string)

        # Log the cleaned string for debugging
        if self.debug:
            logger.debug(f"Cleaned string: {repr(string)}")

        # Step 4: Attempt to parse as JSON
        try:
            parsed_dict = self.parse_as_json(string)
            return parsed_dict
        except json.JSONDecodeError as json_err:
            logger.debug(f"json.loads failed with error: {json_err}")
            # Step 5: Attempt to parse with ast.literal_eval
            try:
                parsed_dict = self.parse_with_literal_eval(string)
                return parsed_dict
            except (SyntaxError, ValueError) as eval_err:
                logger.error(f"Both json.loads and ast.literal_eval failed. Errors: {json_err}, {eval_err}")
                return None

    def string_to_dict_list(self, string: str) -> list:
        """
        Extracts multiple dictionaries from a string and converts each to a Python dictionary.

        Args:
            string (str): The input string containing one or more dictionaries.

        Returns:
            list: A list of parsed dictionaries, or None if parsing fails.
        """
        # Step 1: Strip surrounding whitespace
        string = self.strip_surrounding_whitespace(string)

        # Step 2: Extract dictionary-like substrings
        dict_strings = re.findall(r'\{[^}]*\}', string)
        dict_list = []

        for dict_str in dict_strings:
            # Clean each dictionary-like string using existing methods
            dict_str = self.strip_surrounding_whitespace(dict_str)
            dict_str = self.remove_embedded_markers(dict_str)
            dict_str = self.ensure_string_starts_and_ends_with_braces(dict_str)

            # Attempt to parse each cleaned dictionary string
            try:
                parsed_dict = self.run(dict_str)
                if parsed_dict is not None:
                    dict_list.append(parsed_dict)
            except Exception as e:
                self.logger.error(f"Error parsing dictionary string: {dict_str}\n{e}")
                return None

        return dict_list if dict_list else None




if __name__ == "__main__":


    a ="{\n    'key': 'SELECT DATE_FORMAT(bills.bill_date, \\'%Y-%m\\') AS month, SUM(bills.total) AS total_spending FROM bills WHERE YEAR(bills.bill_date) = 2023 GROUP BY DATE_FORMAT(bills.bill_date, \\'%Y-%m\\') ORDER BY month;'\n}"
    b  = '{\n    "key": "SELECT DATE_FORMAT(bills.bill_date, \'%Y-%m\') AS month, SUM(bills.total) AS total_spending FROM bills WHERE YEAR(bills.bill_date) = 2023 GROUP BY DATE_FORMAT(bills.bill_date, \'%Y-%m\') ORDER BY month;"\n}'
    c= "{\n    'key': 'SELECT DATE_FORMAT(bill_date, \\'%Y-%m\\') AS month, SUM(total) AS total_spendings FROM bills WHERE YEAR(bill_date) = 2023 GROUP BY month ORDER BY month;'\n}"
    d= '{\n    \'key\': "SELECT DATE_FORMAT(bill_date, \'%Y-%m\') AS month, SUM(total) AS total_spendings FROM bills WHERE YEAR(bill_date) = 2023 GROUP BY DATE_FORMAT(bill_date, \'%Y-%m\') ORDER BY DATE_FORMAT(bill_date, \'%Y-%m\');"\n}'
    e= '{   \'key\': "https://dfasdfasfer.vercel.app/"}'

    s2d = String2Dict(debug=True)
    result = s2d.run(e)
    print(result["key"])