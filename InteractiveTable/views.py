from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import pandas as pd 
import json

def background_colors(value):
    if value == 'Pass - 1':
        return 'background-color: green; color: rgba(0, 128, 0, 0); user-select: none'
    elif value == 'Fail - 1':
        return 'background-color: red; color: rgba(255, 0, 0, 0); user-select: none'
    elif value == 'Pass - 0':
        return 'background-color: grey; color: rgba(0, 0, 0, 0); user-select: none'
    else:
        return 'background-color: white; color: rgba(255, 255, 255, 0); user-select: none'

def interactive_grid(request):
    #Read in CSV
    df = pd.read_csv('wafer-tables.csv')
    #print(df)
    
    # Turn CSV into pivot table
    df['Combined'] = df['Verdict'] + ' - ' + df['Availability'].astype(str)
    df_pivot = pd.pivot_table(df, values='Combined', index='Row', columns='Col', aggfunc='sum')

    df_pivot.columns = df_pivot.columns.get_level_values(0)

    # Apply background_colors
    styled_df = df_pivot.style.applymap(background_colors)

    #print(df_pivot)
    
    #Display the DataFrame to HTML
    #Style the table where it removes the column headers
    html_table = styled_df.to_html(classes='table table-bordered', header=False, index=False, table_styles=[
        dict(selector='thead', props=[('display', 'none')]),
        dict(selector='tbody tr th', props=[('display', 'none')]),
    ])
    return render(request, 'getInteractive.html', {'html_table': html_table})
    #return redirect('confirmation')
 

def update_grid(request):
    # Checks if the user sent a POST Request
    if request.method == 'POST':
        updated_data = request.POST.get("updated_data", "")
        grid_data = json.loads(updated_data)
        print(grid_data)
        # Reads again from CSV
        df = pd.read_csv('wafer-tables.csv')
        df_dict = df.to_dict(orient='split')
        df_json = json.dumps(df_dict)
        #print(df_dict)
        
        # Finds the cell that has been selected and it will update the Availability of the selected cell from 1 to 0.
        # If not then it will print on which cell got selected
        for cell in grid_data:
            cell_index = next((index for index, row in enumerate(df_dict['data']) if row[0] == cell["row"] and row[1] == cell["col"]), None)
            if cell_index is not None:
                df_dict['data'][cell_index][3] = 0
                df.loc[cell_index,"Availability"] = 0
            else:
                print(cell["row"])
                print(cell["col"])
        
        #print(df_dict)
        #print(df)
        
        #Saves to CSV
        df.to_csv('wafer-tables.csv', index=False)
        #Reads into csv agin
        df = pd.read_csv('wafer-tables.csv')
        
        # Turn CSV into pivot table
        df['Combined'] = df['Verdict'] + ' - ' + df['Availability'].astype(str)
        df_pivot = pd.pivot_table(df, values='Combined', index='Row', columns='Col', aggfunc='sum')

        df_pivot.columns = df_pivot.columns.get_level_values(0)

        # Apply background_colors
        styled_df = df_pivot.style.applymap(background_colors)

        #print(df_pivot)
        
        #Display the DataFrame to HTML
        #Style the table where it removes the column headers
        html_table = styled_df.to_html(classes='table table-bordered', header=False, index=False, table_styles=[
            dict(selector='thead', props=[('display', 'none')]),
            dict(selector='tbody tr th', props=[('display', 'none')]),
        ])
        return render(request, 'getInteractive.html', {'html_table': html_table})
    else:
        # If empty, display an error message
        return JsonResponse({'error': 'Invalid request method'})
    
def confirmation(request):
    if request.method == 'POST':
        # Get selected cell data from user selection
        updated_data = request.POST.get('updated_data', "")
        print(updated_data)  # Print the received data for debugging
        
        #grid_data = json.loads(updated_data)
        #print(grid_data)

        #return render(request, 'confirmation.html', {'grid_data': grid_data})
        return render(request, 'confirmation.html', {'updated_data': updated_data})
    else:
        # Render the initial confirmation page
        return render(request, 'confirmation.html')
