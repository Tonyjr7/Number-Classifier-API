from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import NumberSerializer


class ClassifyNumbersView(APIView):
    renderer_classes = [JSONRenderer]
    serializer_class = NumberSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to classify a number and return its properties.
        """
        number_str = request.GET.get('number')

        if number_str is None:
            return Response({"error": True}, status=400)

        if not number_str.lstrip('-').isdigit():
            return Response({"number": number_str, "error": True}, status=400)

        number = int(number_str)
        abs_number_str = str(abs(number))

        # Calculate the sum of digits, keeping track of negative numbers
        digit_sum = sum(int(digit) for digit in abs_number_str)
        if number < 0:
            digit_sum = f"-{digit_sum}"

        fun_fact = self.get_fun_fact(number)
        properties = self.get_properties(number)

        data = {
            "number": number,
            "is_prime": self.is_prime(number),
            "is_perfect": self.is_perfect(number),
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def get_fun_fact(self, number):
        """
        Retrieves a fun fact about the given number from an external API.
        """
        try:
            url = f"http://numbersapi.com/{number}/math"
            response = requests.get(url)
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error fetching fun fact: {str(e)}"

    def get_properties(self, number):
        """
        Determines key mathematical properties of the number.
        """
        properties = []
        if self.is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 != 0 else "even")
        return properties

    def is_prime(self, num):
        """
        Checks if a number is prime.
        """
        if num < 2:
            return False
        for i in range(2, int(abs(num) ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def is_perfect(self, num):
        """
        Checks if a number is perfect (sum of its divisors equals itself).
        """
        if num < 1:
            return False
        return sum(digit for digit in range(1, num) if num % digit == 0) == num

    def is_armstrong(self, num):
        """
        Checks if a number is an Armstrong number.
        """
        num_str = str(abs(num))
        power = len(num_str)
        return sum(int(digit) ** power for digit in num_str) == abs(num)
