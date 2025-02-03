from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import NumberSerializer


class ClassifyNumbersView(APIView):
    """
    API View to classify a number based on mathematical properties
    such as prime, perfect, Armstrong, odd, and even status.
    """
    renderer_classes = [JSONRenderer]
    serializer_class = NumberSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to classify a number and return its properties.
        """
        number_str = request.GET.get('number')

        # Check if the number parameter is missing or invalid
        if number_str is None:
            return Response({"error": True}, status=400)

        if not number_str.isdigit():
            return Response({"number": number_str, "error": True}, status=400)

        number = int(number_str)

        # Check if the number is negative
        if number < 0:
            return Response({"number": number_str, "error": True}, status=400)

        # Fetch fun fact about the number from NumbersAPI
        fun_fact = self.get_fun_fact(number)

        # Compute number properties (prime, perfect, Armstrong, odd/even)
        properties = self.get_properties(number)

        # Compute the sum of digits
        digit_sum = sum(int(digit) for digit in number_str)

        # Prepare data for the response
        data = {
            "number": number,
            "is_prime": self.is_prime(number),
            "is_perfect": self.is_perfect(number),
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }

        # Serialize and return the response
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def get_fun_fact(self, number):
        """
        Retrieves a fun mathematical fact for the given number from NumbersAPI.
        """
        try:
            url = f"http://numbersapi.com/{number}/math"
            response = requests.get(url)
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error fetching fun fact: {str(e)}"

    def get_properties(self, number):
        """
        Determines the properties of the number (Armstrong, odd, even).
        """
        properties = []
        if self.is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 != 0 else "even")
        return properties

    def is_prime(self, num):
        """
        Checks if the given number is a prime number.
        """
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def is_perfect(self, num):
        """
        Checks if the given number is a perfect number.
        """
        if num < 1:
            return False
        return sum(digit for digit in range(1, num) if num % digit == 0) == num

    def is_armstrong(self, num):
        """
        Checks if the given number is an Armstrong number.
        """
        num_str = str(num)
        power = len(num_str)
        return sum(int(digit) ** power for digit in num_str) == num
