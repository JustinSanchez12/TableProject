from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd 
import json

def interactive_grid(request):
    # Creates DataFrame of a 3x3 Table
    data = {'Column 1': ['Green', 'Green', 'Green'],
            'Column 2': ['Green', 'Green', 'Green'],
            'Column 3': ['Green', 'Green', 'Green']}
    
    # Reads the DataFrame
    df = pd.DataFrame(data)
    # Displays it to HTML
    html_table = df.to_html(classes='table table-bordered', index=False)

    # Renders the page on templates folder
    return render(request, 'getInteractive.html', {'html_table': html_table})

def update_grid(request):
    #Checks if user sent a POST Request
    if request.method == 'POST':
        updated_data = request.POST.get('updated_data', '')
        
        try:
            # Converts JSON data into a python object
            grid_data = json.loads(updated_data)
            # Recreates original table
            df = pd.DataFrame({
                'Column 1': [grid_data[i] for i in [0, 3, 6]],
                'Column 2': [grid_data[i] for i in [1, 4, 7]],
                'Column 3': [grid_data[i] for i in [2, 5, 8]]
            })

            # Updates table to HTML - This should act as updated table with changes
            html_table = df.to_html(classes='table table-bordered', index=False)
            # Renders to the templates
            return render(request, 'getInteractive.html', {'html_table': html_table})
        except json.JSONDecodeError:
            # If JSON can't convert to python object
            return JsonResponse({'error': 'Invalid JSON Data'})
    else:
        # If empty displays error message
        return JsonResponse({'error': 'Invalid request method'})