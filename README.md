## Description
The objective of this project is to build a Semiconductor Wafer Application that runs in the browser. This application is to simulate a worker being able to select which dye of a silicon wafer is being used to make
a semiconductor. When the user opens the application, a web browser will appear it will be shown a grid with squares that are red or green. Green are represented as "pass" dyes and red are the "failed" dye. When a dye is selected
it will change colors from green/red to white. After the user selects the dye it will display a confirmation page where once selected yes, it will return back to the first page but it will update the availability of the 
dye previously selected. 

In this example, data is being read from a .csv file using pandas with columns labeled rows, cols, and availability. This represents the coordinates of the squares on the grid. When the user updates the grid table, then the 
.csv file will be updated changing the availability of the squares selected from 1 -> 0 indicating there is no more in stock. 

## Technology Used
- Dataframe: Pandas
- Framework: Django  
