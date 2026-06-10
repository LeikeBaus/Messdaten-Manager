from datetime import datetime

from model.measurement_data import MeasurementData


class Experiment:

    def __init__(self,
                 experiment_id, name: str,
                 description: str = "",            #Bei der Import unvollständige Datein, nicht zwingend übergeben
                 date: datetime = None):  #---||---

        self.experiment_id = experiment_id
        self.name = name
        self.description = description if description is not None else "" #"None" aus dem Konstruktor
        self.date = date if date is not None else datetime.now()

        self.measurements = {}

    def add_measurement(self, measurement: MeasurementData):
        if measurement is not None:  # Falls beim Import etwas schiefgeht
            key = measurement.name
            self.measurements[key] = measurement

    def get_measurement(self, name) -> MeasurementData | None:
        return self.measurements.get(name)

    # Liste von alle Messungen in einem Versuch
    def get_all_measurements_names(self):
        return list(self.measurements.keys())

    def __repr__(self) -> str:
        return (f"Experiment( ID: {self.experiment_id}, name: {self.name}, "
                f"measurements: {self.get_all_measurements_names()})")

if __name__ == "__main__":
    experiment_1 = Experiment("exp_01", "Material test")
    experiment_2 = Experiment("exp_02", "Temperature and Force test",
                              "Iron temperature control", datetime.now())
    print(experiment_1)
    print(experiment_2)

    test_obj_21 = MeasurementData("Temperature", unit="°C", values=[21.5, 22, 23.1, 22.1])
    test_obj_22 = MeasurementData("Force", unit="N", values=[15, 23.7, 28.3, 37.9])

    experiment_2.add_measurement(test_obj_21)
    experiment_2.add_measurement(test_obj_22)

    print("Current measurements at ID: ",experiment_2.experiment_id,"\n",
          experiment_2.get_all_measurements_names())