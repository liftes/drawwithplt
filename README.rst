PythonDraw
==========
Provides an encapsulation of common functions for scientific drawing.

Includes: Font uniform settings: Chinese display and font font size settings, Chinese Song script, Spanish New Rome;

Color uniform setting: use the cmap color card to return colorlist;

Quickly save pictures: unified dpi=1200; and set the bool value to facilitate unified control over whether to save.

Heat map drawing: contour lines, coordinate axis correction

3D plotting: contour lines and projections

Spline interpolation etc...

========
.. code:: python

   # Import the necessary drawing libraries
   from Draw import plt,sns
   import Draw as D

   # Set the color
   color_list = D.SetColor('tab20',np.linspace(0, 1, 10))

   # Dictionary controls and code examples drawn using heat maps:
   xdict = {"name": "ylabel", "step": 5,"start":1, "fmt":"%.0f"}
   ydict = {"name": "xlabel", "step": 5, "angle":0, "fmt":"%.0f"}
   zdict = {"name": "Random"}
   x = np.array(range(32))
   y = np.array(range(32))
   z = np.random.randint(0,10,(32,32))
   D.snsFix(x, y, z, xl=xdict, yl=ydict, zl=zdict,
            normalZero=True, contour=False)

Update: (2022-4-30)
-------------------

It provides a quick entry for customizing default parameters, provides custom gradient colors and color card displays, improves the drawing module of heat map, and opens a custom setting interface for colorbar.