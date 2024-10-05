import traceback
import freecurrencyapi
import csv
import datetime
import json
import os
import logging as logger

# Set up logging
logger.basicConfig(level=logger.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')


class TokenAnalysis:
    """
    A class to analyze token usage and calculate the cost of token usage for various LLMs like OpenAI and Anthropic.

    Attributes:
    -----------
    config_path : str
        Path to the JSON file containing the pricing information for different models.
    api_key : str
        API key for live currency conversion via freecurrencyapi. If not provided, default exchange rates will be used.
    output_currency : str
        The output currency in which to calculate the cost (default is INR).
    output_csv : str
        The path where the output CSV will be stored. If not provided, the CSV will be created in the root directory.
    create_csv : bool
        Flag indicating whether to create a CSV file for storing the results (default is True).
    log_info : bool
        Flag indicating whether to print log information about the token cost (default is True).

    Methods:
    --------
    token_analysis(response: dict, client: str, module_name="Not Provided"):
        Calculates the token cost based on the provided response data and writes it to a CSV if `create_csv` is True.
    """

    def __init__(self, config_path='analyzer/config.json', api_key=None, output_currency="INR", output_csv=None, create_csv=True, log_info=True):
        """
        Initializes the TokenAnalysis object by loading configuration data, setting up currency exchange rates,
        and initializing logging options.

        Parameters:
        -----------
        config_path : str
            Path to the JSON config file.
        api_key : str
            API key for freecurrencyapi. You can generate one by signing up here: https://app.freecurrencyapi.com/login
        output_currency : str
            The currency in which the output cost will be calculated (default is INR).
        output_csv : str
            The path where the CSV file will be stored. If not provided, the file will be created in the root directory.
        create_csv : bool
            Whether to create a CSV file (default is True).
        log_info : bool
            Whether to log the calculated costs (default is True).
        """
        self.create_csv = create_csv
        self.log_info = log_info
        self.output_csv = output_csv if output_csv else 'token_analysis.csv'

        # Load the configuration data
        try:
            with open(config_path) as json_file:
                self.llm_config_data = json.load(json_file)
            logger.debug("Configuration file loaded successfully.")
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            self.llm_config_data = {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON configuration: {e}")
            self.llm_config_data = {}

        # Initialize currency settings
        self.output_currency = output_currency.upper()  # Default is INR
        self.default_exchange_rate = {
            "INR": 84, "USD": 1, "EUR": 0.92}  # Add default rates
        self.exchange_rate = self.default_exchange_rate.get(
            self.output_currency, 84)

        # Initialize the currency client if API key is provided
        if api_key:
            try:
                self.currency_client = freecurrencyapi.Client(api_key)
                self.currency_data = self.currency_client.latest()  # Get the latest currency data
                self.exchange_rate = self.currency_data.get(
                    self.output_currency, self.exchange_rate)
                logger.info(
                    f"Currency exchange rate for {self.output_currency} fetched successfully: {self.exchange_rate}")
            except Exception as e:
                logger.error(
                    f"Failed to initialize currency client or fetch data: {traceback.format_exc()}")
                logger.warning(
                    f"Using default exchange rate for {self.output_currency}: {self.exchange_rate}")
        else:
            logger.warning(
                f"No API key provided. Using default exchange rate for {self.output_currency}: {self.exchange_rate}")

    def token_analysis(self, response: dict, client: str, module_name="Not Provided"):
        """
        Analyzes token usage and calculates the cost based on the input/output tokens and model information.
        Optionally writes the results to a CSV file or logs the output based on the flags.

        Parameters:
        -----------
        response : dict
            The response data containing the token usage information.
        client : str
            The name of the client (e.g., "OPENAI", "ANTHROPIC").
        module_name : str
            The name of the module from which the request originated (default is "Not Provided").

        Returns:
        --------
        float : The total calculated cost.
        """
        try:
            prompt_count = None
            completion_count = None
            model_name = None

            # Set the exchange rate for output currency
            exchange_rate = self.exchange_rate

            # Extract token usage and model name based on the client
            if client == "OPENAI":
                prompt_count = response.usage.prompt_tokens
                completion_count = response.usage.completion_tokens
                model_name = response.model
            elif client == "ANTHROPIC":
                prompt_count = response.get("usage").get("input_tokens")
                completion_count = response.get("usage").get("output_tokens")
                model_name = response.get("model")

            # Fetch the pricing data for the model
            pricing_data = self.llm_config_data.get(
                client, {}).get(model_name, None)

            if pricing_data is None:
                logger.warning(
                    f"Pricing data for {client} model {model_name} not found.")
                return

            # Calculate prompt and completion costs
            prompt_cost = round((prompt_count / 1000) *
                                pricing_data['input_cost'] * exchange_rate, 2)
            completion_cost = round(
                (completion_count / 1000) * pricing_data['output_cost'] * exchange_rate, 2)
            total_cost = prompt_cost + completion_cost

            # Log the calculated costs if logging is enabled
            if self.log_info:
                logger.info(f"""Costs in {self.output_currency} [Exchange Rate : {exchange_rate}]
                    Input : {prompt_cost} ({prompt_count} Tokens)
                    Output : {completion_cost} ({completion_count} Tokens)
                    Total : {total_cost}
                    """)

            # Write to CSV if the flag is set
            if self.create_csv:
                if not os.path.exists(self.output_csv):
                    with open(self.output_csv, mode='w') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Timestamp', 'Model Name', 'Prompt Tokens',
                                         'Prompt Cost', 'Completion Tokens', 'Completion Cost', 'Total Cost', 'Module Name'])

                with open(self.output_csv, mode='a') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.datetime.now(), model_name, prompt_count,
                                     prompt_cost, completion_count, completion_cost, total_cost, module_name])

            return total_cost

        except Exception as e:
            logger.debug(
                f"An unexpected error occurred: {traceback.format_exc()}")
            return None
