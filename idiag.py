# coding: utf-8
# In[32]:
from pymongo import MongoClient, DESCENDING
from bokeh.models import Range1d, LinearAxis, ColumnDataSource, BoxAnnotation, HoverTool, SaveTool, CrosshairTool, BoxZoomTool, ResetTool
from bokeh.plotting import figure #, output_file
from bokeh.io import curdoc

TOOLS = [HoverTool(tooltips=[("t", "$x"), ("y", "$y")]), SaveTool(), CrosshairTool(), BoxZoomTool(), ResetTool()]


client = MongoClient()
db = client['localhost:27017']
data = db.injections.find_one({'Mac':'B630T1'},sort=[('_id',DESCENDING)])

## Configuration du graphique
fig = figure(plot_width=1700, plot_height=800, tools=TOOLS)

# axe x temps
fig.xaxis.axis_label = 'Temps [ms]'

# axe Course S
fig.yaxis.axis_label = 'Course [mm]'
fig.yaxis.axis_label_text_color= 'green'
fig.y_range = Range1d(start=0, end=1000)

# axe vitesse V
fig.extra_y_ranges['V'] = Range1d(start=0, end=5)
fig.add_layout(LinearAxis(y_range_name='V', axis_label='Vitesse [m/s]', axis_label_text_color='blue'), 'left')

# axe pression P
fig.extra_y_ranges['P'] = Range1d(start=0, end=300)
fig.add_layout(LinearAxis(y_range_name='P', axis_label='Pression [bar]', axis_label_text_color='red'), 'right')

#Grille
fig.ygrid.minor_grid_line_alpha = 10
box1 = BoxAnnotation(left=1560, right=1950, fill_color='green', fill_alpha=0.02)
fig.add_layout(box1)

box2 = BoxAnnotation(bottom=650, top=700, fill_color='green', fill_alpha=0.02)
fig.add_layout(box2)

#Couleurs
#fig.background_fill_color = "beige"
#fig.border_fill_color = "whitesmoke"i

##donnees
#data = {'T': range(0, 3000, 5),
#        'S': ,
#        'V': ,
#        'P': }
source = ColumnDataSource(dict(T=range(0,3000,2), S=data['S'], V=data['V'], P=data['P']))
#source.trigger("change")
##lignes
fig.line(
    x = 'T',
    y = 'S',
    legend = 'Course',
    color = 'green',
    source = source
)

fig.line(
    x = 'T',
    y = 'V',
    legend = 'Vitesse',
    y_range_name = 'V',
    color = 'blue',
    source = source
)

fig.line(
    x = 'T',
    y = 'P',
    legend = 'Pression',
    y_range_name = 'P',
    color = 'red',
    source = source
)

def update():
    data = db.injections.find_one({'Mac':'B630T1'},sort=[('_id',DESCENDING)])


#Affichage
fig.toolbar_location = 'above'
curdoc().add_root(fig)

curdoc().add_periodic_callback(update, 50)
curdoc().title = data['Mac'] + " " + data['Date']
