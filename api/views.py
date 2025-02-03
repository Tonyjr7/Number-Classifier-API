from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
import re

from api.serializers import NumberSerializer

# Set up logging
logging.basicConfig(level=logging.INFO)

NUMBERS_API_URL = 'http://numbersapi.com/{}/math?json=true'

class ClassifyNumbersView(APIView):
    renderer_classes = [JSONRenderer]
    serializer_class = NumberSerializer

    def get(self, request, *args, **kwargs):
        # Get the 'number' query parameter from the request
        number_str = request.GET.get('number')

        # If number is not provided or is empty, return an error
        if not number_str:
            return Response({'error': 'Please provide a number using the "number" query param.'}, status=400)

        # Validate the input number format using regex
        if not re.match(r"^-?\d+$", number_str):
            return Response({"number": number_str, "error": True}, status=400)

        try:
            # Parse the number from the string
            number = int(number_str)
        except ValueError:
            return Response({"number": number_str, "error": True}, status=400)

        # If the number is negative, return error
        if number < 0:
            return Response({"number": number_str, "error": True}, status=400)

        # Query the Numbers API
        try:
            num_response = requests.get(NUMBERS_API_URL.format(number))
            num_response.raise_for_status()  # Raise an error for bad responses
            num_data = num_response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return Response({"error": "API request failed", "details": str(e)}, status=500)

        # Checking number properties
        prime = self.is_prime(abs(number))
        perfect = self.is_perfect(abs(number))
        sum_digits = self.digit_sum(number)
        properties = self.get_properties(number)

        # Combining all the data
        combined_data = {
            'number': number,
            'is_prime': prime,
            'is_perfect': perfect,
            'properties': properties,
            'digit_sum': sum_digits,
            'fun_fact': num_data.get('text', 'No fun fact available'),
        }

        # Serialize and return the response
        serializer = self.serializer_class(data=combined_data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    # Check if the number is prime
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    # Check if the number is perfect
    def is_perfect(self, n):
        if n < 2:
            return False
        divisors = [i for i in range(1, n) if n % i == 0]
        return sum(divisors) == n

    # Calculate the sum of digits
    def digit_sum(self, n):
        return sum(int(digit) for digit in str(abs(n)))

    # Get properties of the number (even/odd, Armstrong)
    def get_properties(self, n):
        properties = []
        if self.is_armstrong(n):
            properties.append("armstrong")
        if n % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")
        return properties

    # Check if the number is an Armstrong number
    def is_armstrong(self, n):
        n = abs(n)
        digits = [int(digit) for digit in str(n)]
        num_digits = len(digits)
        return sum(digit ** num_digits for digit in digits) == n
