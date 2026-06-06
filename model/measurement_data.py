import numpy as np

class MeasurementData:

    def __init__(self, name: str, unit: str, values: list | np.ndarray ) :
        # list: Daten kommen von außen (JSON, GUI-Einzeltabellen)
        # np.ndarray: Daten innerhalb der Logik (aus interne Berechnungen)
        self.name = name
        self.unit = unit

        # values in NumPy-Array konvertieren, wenn es eine Liste ist
        self.values = np.asarray(values, dtype=float)

    def __repr__(self) -> str:
        return f"MeasurementData(Name: {self.name}, unit:{self.unit}, values: {len(self.values)})"

if __name__ == "__main__":
    test_obj = MeasurementData("Temperatur", unit="°C", values=[21.5,22,23.1,22.1])
    print(test_obj)
    print(test_obj.values)
    print("NumPy-Array Typ:", type(test_obj.values))