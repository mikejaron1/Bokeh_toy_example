from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import TextInput, Div
from bokeh.models import CustomJS, WidgetBox, ColumnDataSource, PrintfTickFormatter
from bokeh.layouts import gridplot, layout

import pandas as pd

data = pd.DataFrame({'cat': [10, 20, 30, 40],
                    'growth': [30, 40, 60, 20]})
x = [1, 2, 3, 4]
y = data['growth']

p = figure(plot_width=400, plot_height=400, x_range=(0, 5), y_range=(0,max(y)+6))

p.vbar(x=x, width=0.5, bottom=0,
       top=y, color="blue", alpha=0.6)

x = [-1]
y = [max(y)+5]

source = ColumnDataSource(data=dict(x=x, y=y))
p.triangle('x', 'y', source=source, size=20, color="orange", alpha=0.8, angle=244)

# p.xaxis[0].formatter = PrintfTickFormatter(format="test")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = CLTV.value;
    var g = cost.value;
    x = data['x']
    y = data['y']
    x[0] = Math.round(f/g)
    source.trigger('change');
""")


text_input1 = TextInput(value="", title="CLTV",  callback=callback)
callback.args["CLTV"] = text_input1

text_input2 = TextInput(value="", title="Cost",  callback=callback)
callback.args["cost"] = text_input2

text = 'Text for option A will go here.'

div = Div(text=text, width=200, height=100)
# div.js_on_change(text, callback)
# callback.args["cost"] = text_input2

widgets = WidgetBox(text_input1, text_input2)

grid = gridplot([widgets, p, div], ncols=2, plot_width=250, plot_height=250)
output_file("bar.html")
show(grid)
