
import pandas as pd
import plotly_express as px
from ydata_profiling import ProfileReport

class PandasDataExplorer:
    def __init__(self, df: pd.DataFrame):
      self.df = df
      self.df = self.df.convert_dtypes()
    
    def clean_columns(self):
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')


    def rename_columns(self,cols: list,new_names: list):
        columns = self.df.columns
        for i in range(len(cols)):
            columns[cols[i]] = new_names[i]
        
        self.df.columns = columns

    
    def remove_columns(self, col_indices):
        """Remove columns from the DataFrame based on a list of column indices."""
        # Get column names corresponding to the provided indices
        col_names_to_remove = [self.df.columns[idx] for idx in col_indices]
        # Drop the columns
        self.df.drop(columns=col_names_to_remove, inplace=True)

    
    def change_column_dtype(self,col_number,type = 'int64'):
        col_name = self.df.columns[col_name]
        self.df[col_name] = self.df[col_name].astype(type)


    def copy(self):
        return self.df.copy()
    
    
    def save_copy(self,filename: str):
        self.df.to_csv(filename,index=False)

    
    def show(self,rows = 5):
        return self.df.head(rows)
    
    
    def get_info(self):
        return self.df.info()

    def convert_dtypes(self):
        self.df = self.df.convert_dtypes()
        
    
    def delete_duplicate_rows(self):
        self.df = self.df.drop_duplicates(keep='first')


    def clean_string_columns(self):
        """
        Select all string columns and apply trim operation to remove unwanted spaces,
        then set all values to lowercase.
        """
        string_columns = self.df.select_dtypes(include=['string','object']).columns
        self.df[string_columns] = self.df[string_columns].apply(lambda x: x.str.strip().str.lower())


    def clean_float_columns(self):
        """
        Select all float columns and round the values to 2 decimal points.
        """
        float_columns = self.df.select_dtypes(include=['float']).columns
        self.df[float_columns] = self.df[float_columns].round(2)


    def parse_date_columns(self):
        """Transform string columns to datetime if they match specific formats."""
        date_formats = [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M",
            "%d-%m-%Y %H:%M:%S"
        ]
        for col_name in self.df.select_dtypes(include=['string','object']).columns:
            for date_format in date_formats:
                try:
                    self.df[col_name] = pd.to_datetime(self.df[col_name], format=date_format)
                    break
                except Exception as e:
                    continue


    def parse_int_columns(self):
    
        for col in self.df.select_dtypes(include=['string','object']).columns:
            try:
                # Try converting the column to numeric
                numeric_col = self.df[col].str.isdigit().all()
                # Check if the conversion was successful for all values
             
                    # If yes, check if all values are integers
                if numeric_col:
                    self.df[col] = self.df[col].astype('int64')
                else:
                    float_col = pd.to_numeric(self.df[col])
                    self.df[col] = float_col.astype('float64')
            except Exception as e:
                # If conversion fails, continue to the next column
                continue


    def convert_to_datetime(self, col_number, fmt):
        
        try:
            # Convert the specified column to date/datetime format
            self.df.iloc[:, col_number] = pd.to_datetime(self.df.iloc[:, col_number], format=fmt)
        except Exception as e:
            print(f"Error occurred while parsing date column: {e}")
    
  
    def find_outliers(self, column_number):
        """Find outliers in a specified column using the IQR method and return them as a df."""
        column_name = self.df.columns[column_number]
        Q1 = self.df[column_name].quantile(0.25)
        Q3 = self.df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = self.df[(self.df[column_name] < lower_bound) | (self.df[column_name] > upper_bound)]
        return outliers
    
    
    def drop_outliers(self, column_number):
        """Find outliers in a specified column using the IQR method and return them as a df."""
        column_name = self.df.columns[column_number]
        Q1 = self.df[column_name].quantile(0.25)
        Q3 = self.df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        self.df = self.df[(self.df[column_name] >= lower_bound) | (self.df[column_name] <= upper_bound)]
        

    def find_missing_values(self,pct: bool = False):
        """
        Calculate and return the sum of missing values for each column in a DataFrame.
        If pct is True, return the missing values as a percentage of the DataFrame's length..
        """
        # Check if pct is True
        if pct:
            # Calculate missing values as a percentage of the DataFrame's length
            missing_pct = (self.df.isnull().sum() / len(self.df)) * 100
            # Sort the values in descending order
            return missing_pct.sort_values(ascending=False)
        
        else:
            # Calculate the sum of missing values for each column
            missing_count = self.df.isnull().sum()
            # Sort the values in descending order
            return missing_count.sort_values(ascending=False)
            
    
    def drop_missing_values(self,cols = None):
        if cols == None:
            self.df.dropna(inplace=True)
        else:
            col_names = [self.df.columns[idx] for idx in cols]
            self.df.dropna(subset=col_names,inplace=True)


    def groupby(self, groupby, col, func = 'sum',sort_descending = True):
        """Group by a specified column and aggregate another column using a specified function."""
        groupby_col = self.df.columns[groupby]
        col_name = self.df.columns[col]
        
        if func == "sum":
            result = self.df.groupby(groupby_col)[col_name].sum().reset_index()
        elif func == "min":
            result = self.df.groupby(groupby_col)[col_name].min().reset_index()
        elif func == "max":
            result = self.df.groupby(groupby_col)[col_name].max().reset_index()
        elif func == "count":
            result = self.df.groupby(groupby_col)[col_name].count().reset_index()
        elif func == "avg":
            result = self.df.groupby(groupby_col)[col_name].mean().reset_index()
        else:
            raise ValueError("Invalid function. Supported values are: sum, min, max, count, avg.")
        
             
        if sort_descending:
            result = result.sort_values(by=col_name, ascending=False)

        return result
    
 
    
    def count_distinct(self, groupby, col):
        """Count distinct values of a column within each group."""
        group_name = self.df.columns[groupby]
        col_name = self.df.columns[col]

        try:
            result = self.df.groupby(group_name)[col_name].nunique().reset_index()
            result = result.sort_values(by=col_name, ascending=False)
        except Exception as e:
            print('An exception occurred: ', str(e))
            result = None
        
        return result

        
        
    def apply_function(self, col_number, func):
        """Apply a given function to a specified column of the DataFrame."""
        col_name = self.df.columns[col_number]
        self.df[col_name] = self.df[col_name].apply(func)
    
    def show_numerical_distribution(self):
        numerical_columns = self.df.select_dtypes(include=['float64', 'int64']).columns

        for single_column in numerical_columns:
            fig = px.histogram(self.df, x=single_column, title=f'Distribution of {single_column}')
    
            # Update figure layout for bigger size
            fig.update_layout(
                width=800,  # Set the width to be larger
                height=600,  # Set the height to be larger
                template="plotly_dark",  # Use dark theme
            )
            
            # Show the figure
            fig.show()
    
    def categorical_unique_values(self):
        string_and_categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns

        # Loop through each column and print the number of unique values
        for col in string_and_categorical_cols:
            unique_count = self.df[col].nunique()
            print(f"'{col}' : has {unique_count} unique values.")
    

    def show_corelation_matrix(self):

        corr_matrix = self.df.corr()
        
        fig = px.imshow(corr_matrix,x=corr_matrix.columns,y=corr_matrix.index,text_auto=True,color_continuous_scale='Blues')
    
        # Update figure layout for bigger size
        fig.update_layout(
            width=800,  # Set the width to be larger
            height=600,  # Set the height to be larger
            template="plotly_dark",  # Use dark theme
        )
        
        # Show the figure
        fig.show()





    
    def perform_initial_cleaning(self):
        self.clean_columns()
        self.clean_float_columns()
        self.clean_string_columns()
        self.delete_duplicate_rows()
        self.parse_date_columns()
        self.parse_int_columns()
    

    def generate_profile_report(self):
        self.perform_initial_cleaning()

        print('generating profile report ....')
        report = ProfileReport(self.df,explorative=True)
        report.to_file('profile-report.html')


    

        


