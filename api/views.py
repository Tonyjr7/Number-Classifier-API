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
        # Get the number
        number_str = request.GET.get('number')

        if number_str is None:
            return Response({"error": True}, status=400)

        if not number_str.lstrip('-').isdigit():
            # Return the response with the parameter
            return Response({"number": number_str, "error": True}, status=400)
        
        number = int(number_str) #convert number to integer

        if number < 0:
            return Response({"number":number_str,"error": True,}, status=400)

        #query the NumbersAPI
        url = f"http://numbersapi.com/{number}/math"
        response = requests.get(url)
        fun_fact = response.text
        
        # Check if the number is prime
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if (num % i) == 0:
                    return False
            return True
            
        # Check if the number is perfect
        def is_perfect(num):
            if num < 1:
                return False
            return sum(digit for digit in range(1, num) if num % digit == 0) == num
        
        # Check if the number is an Armstrong number
        def is_armstrong(num):
            num_str = str(num)
            power = len(num_str)
            return sum(int(digit) ** power for digit in num_str) == num
        
        # Compute values        
        check_prime_status = is_prime(number)
        check_perfect_status = is_perfect(number)
        check_armstrong_status = is_armstrong(number)
        digit_sum = sum(int(digit) for digit in number_str)
        
        # Add properties to response
        properties = []
        if check_armstrong_status is True:
            properties.append("is_armstrong")
        if number % 2 != 0:
            properties.append("odd")
        else:
            properties.append("even")

        #formatting data to serialze
        data = {
            "number" : number,
            "is_prime" : check_prime_status,
            "is_perfect" : check_perfect_status,
            "properties" : properties,
            "digit_sum" : digit_sum,
            "fun_fact" : fun_fact
        }

        # Serialize the data and return it
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        

        

