from dataclasses import dataclass, field

@dataclass
class MeasurementData:
	"""Store raw tabular measurement values and helper conversions."""

	headers: list[str] = field(default_factory=list)
	rows: list[list] = field(default_factory=list)

	def _parse_number(self, value):
		# Accept both decimal separators from imported files.
		text = str(value).strip().replace('"', "")
		text = text.replace(",", ".")
		return float(text)

	def numeric_xy_series(self, x_column=0, y_column=1):
		# Convert two selected columns into numeric x/y vectors.
		x_values = []
		y_values = []

		for row in self.rows:
			x_value = self._parse_number(row[x_column])
			y_value = self._parse_number(row[y_column])
			x_values.append(x_value)
			y_values.append(y_value)

		return x_values, y_values


@dataclass
class MeasurementSeries:
	"""Represent one named measurement including axis and plot metadata."""

	id: str
	name: str
	data: MeasurementData = field(default_factory=MeasurementData)
	x: dict = field(default_factory=dict)
	y: dict = field(default_factory=dict)
	plot: dict = field(default_factory=dict)


@dataclass
class Experiment:
	"""Represent one experiment with metadata and a list of measurements."""

	id: str
	metadata: dict = field(default_factory=dict)
	measurements: list[MeasurementSeries] = field(default_factory=list)