from abc import ABC
from concurrent.futures import ThreadPoolExecutor


class Requests(ABC):
    @staticmethod
    def parallelRequests(data):
        dataCopy = data.copy()
        with ThreadPoolExecutor() as executor:
            futures = []
            for key, task in dataCopy.items():
                futures.append(executor.submit(task["functor"], *task["params"]))

            results = [future.result() for future in futures]
            for key, result in zip(dataCopy.keys(), results):
                dataCopy[key]["result"] = result

            return dataCopy
