import Functions.GetParameters as gp
import datetime

def get_URL_params():
    final_params=''
    Error = True
    while Error:
        try:
            print('--------------------------------------------------------------------')
            other_params= [0]
            if max(other_params) > 1 or min(other_params) < 0:
                raise ValueError

            category_list = list(map(str,input("Enter different categories separated by commas* (Required)\nExample -> Web Development,Accounts,Acting\n").split(','))) #Example -> Web Development,Accounts,Acting
            location_list = list(map(str,input("Enter different locations separated by commas* (Required)\nExample -> Mumbai,Delhi\n").split(','))) #Example -> Mumbai,Delhi
            
            start = []
            
            duration = []
            print('--------------------------------------------------------------------')
            Error = False
        except (ValueError,IndexError,TypeError):
            print("Error in input values, loading options again")
            Error = True
  
    if other_params == 1:
        final_params += '/internships-for-women/'
    else:
        final_params += '/internships/'

    start_date,max_duration = gp.select_dates(start,duration)

    final_params += gp.select_categories(category_list)
    final_params += gp.select_locations(location_list)
    final_params += max_duration
    final_params += start_date
    
    return final_params

if __name__ == "__main__":
    print("Run main.py file")
     