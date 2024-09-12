from django.shortcuts import render
from django.views import View
from .models import Problem, InputOutput
from customtest.forms import CodeSubmissionForm
from globals.executor import CodeExecutor


class ProblemsView(View):
    def get(self, request):
        fetched_problems = Problem.objects.all()
        return render(request, 'problems/problems.html', {'fetched_problems': fetched_problems})
    
    def post(self, request):
        pass


class FetchProblemView(View):
    def get(self, request, id):
        problems = Problem.objects.filter(id=id)
        test_cases = InputOutput.objects.filter(problem=problems[0].id)
        context = {
            'fetched_problem': problems,
            'test_cases': test_cases,
            'form': CodeSubmissionForm()
        }
        return render(request, 'problems/individual_problem.html', context)
    
    def post(self, request, id):
        source_code = request.POST['code']
        language = request.POST['language']
        ios = InputOutput.objects.filter(problem=Problem.objects.filter(id=id)[0])
        test_cases = []
        for element in ios:
            test_cases.append([element.input, element.output, element.problem.time_limit])
        

        for case in test_cases:
            executor = CodeExecutor()
            if language == "0":
                output = executor.execute_c_code(source_code, case[0], case[2])
            elif language == "1":
                output = executor.execute_cpp_code(source_code, case[0], case[2])
            elif language == "2":
                output = executor.execute_python_code(source_code, case[0], case[2])

            if output[0].strip() != case[1].strip():
                context = {
                    'output': f"Test case failed:\nInput: {case[0]}\nExpected: {case[1]} \n\n\nReceived: {output}",
                    'time': "Execution time: " + output[1] + " seconds"
                }
                return render(request, 'customtest/output.html', context)
    
        context = {
            'output': "All test cases passed",
            'time': "Execution time: " + output[1] + " seconds"
        }
        return render(request, 'customtest/output.html', context)
