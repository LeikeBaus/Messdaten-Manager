from dataclasses import dataclass, field

@dataclass
class MeasurementData:
	headers: list[str] = field(default_factory=list)
	rows: list[list] = field(default_factory=list)

	def _parse_number(self, value):

		text = str(value).strip().replace('"', "")
		text = text.replace(",", ".")
		return float(text)

	def numeric_xy_series(self, x_column=0, y_column=1):
		x_values = []
		y_values = []

		for row in self.rows:
			x_value = self._parse_number(row[x_column])
			y_value = self._parse_number(row[y_column])
			x_values.append(x_value)
			y_values.append(y_value)

		return x_values, y_values
