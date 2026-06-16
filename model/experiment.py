from dataclasses import dataclass, field

from model.measurement_data import MeasurementData


@dataclass
class MeasurementSeries:
	id: str
	name: str
	data: MeasurementData = field(default_factory=MeasurementData)
	x: dict = field(default_factory=dict)
	y: dict = field(default_factory=dict)
	plot: dict = field(default_factory=dict)


@dataclass
class Experiment:
	id: str
	metadata: dict = field(default_factory=dict)
	measurements: list[MeasurementSeries] = field(default_factory=list)
