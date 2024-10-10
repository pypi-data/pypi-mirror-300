# uggo
## Tastefully Ugly Charts!
Just a fun experiment on making my own charting library using just [PIL/pillow](https://python-pillow.org/).

```sh
pip install uggo
```

You can also fiddle with the code and install the package locally.

```sh
pip install -e .
```

## Usage
```python
import uggo

# Example data
data = [10, 20, 15, 25, 30]
labels = ['A', 'B', 'C', 'D', 'E']
x_label = "Categories"
y_label = "Values"

# Create and show pie chart
pie_chart = uggo.PieChart(width=500, height=500, data=data, labels=labels, title="Pie Chart")
pie_image = pie_chart.draw()
pie_image.save("piechart.png")

# Create and show line chart
line_chart = uggo.LineChart(500, 400, data, labels, x_label, y_label, title="Line Chart")
line_image = line_chart.draw()
line_image.save("linechart.png")

# Create and show bar chart
bar_chart = uggo.BarChart(500, 400, data, labels, x_label, y_label, gap_percentage=0.2, title="Bar Chart")
bar_image = bar_chart.draw()
bar_image.save("barchart.png")
```

## Examples
![Bar Chart](./barchart.png)

![Line Chart](./linechart.png)

![Pie Chart](./piechart.png)
