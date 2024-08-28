import pandas as pd
from extract_area_of_interest import extract_area_of_interest
from calculate_head import calculate_head

def update_hydropower_plant_data(xlsx_file, dem_path, flow_path, flow_acc_path):
    df = pd.read_excel(xlsx_file)

    for index, row in df.iterrows():
        if pd.isna(row['head']):
            dem, flow, flow_acc, window = extract_area_of_interest(
                dem_path, flow_path, flow_acc_path, 
                row['latitude'], row['longitude']
            )
            head = calculate_head(dem, flow, flow_acc)
            df.at[index, 'head'] = head
    
    # Save the updated dataframe
    df.to_excel("updated_hydropower_plants.xlsx", index=False)

    return df