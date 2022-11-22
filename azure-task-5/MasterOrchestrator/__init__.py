# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt


import azure.durable_functions as df
import azure.functions as func


def orchestrator_function(context: df.DurableOrchestrationContext):
    # Get a list of N work items to process in parallel.

    dictionaries = yield context.call_activity("DataFetcher", "")
    # print(dictionaries)

    reduced_files = {}
    for dic in dictionaries.items():
        mapped_lines_combined = []
        tasks = []
        for dict_line in dic[1]:
            for key, val in dict_line.items():
                tasks.append((key, val))
        for tuple in tasks:
            F1= yield context.call_activity("Mapper", (tuple[0], tuple[1]))
            mapped_lines_combined.append(F1)
        m = yield context.call_activity("Shuffler", mapped_lines_combined)
        temp = []
        for f in m.items():
            temp.append(context.call_activity("Reducer", f))
        results = yield context.task_all(temp)
        reduced_files[dic[0]] = results

    print(reduced_files)
    return reduced_files

    # F1 = yield context.call_activity("Mapper", (x,y))
    # F1 = yield context.call_activity("Mapper", (1,line))
    # m = yield context.call_activity("Shuffler",F1)
    #temp = []
    # for f in m.items():
    #    temp.append(context.call_activity("Reducer",f))

    # results = yield context.task_all(temp)


main = df.Orchestrator.create(orchestrator_function)
