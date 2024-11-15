from dataCRUD import dataProcessing
from dataCLEANING import *

def ShowMenu():
    print ("\n       +---------------------DATA EXECUTION---------------------+")
    print ("       |                    0. Exit Program                     |")
    print ("       | 1. Display Data Sheet            4. Delete Data Record |")
    print ("       | 2. Add New Data Record           5. Save Data Record   |")
    print ("       | 3. Update Data Record            6. Clean Data         |")
    print ("       |________________________________________________________|")

def main():
    Data_File = 'StudentPerformanceFactors.csv'
    outfileDataCleaned = "cleaned_StudentPerformanceFactors.csv"
    Data_Frame = dataProcessing(Data_File)

    while True:
        # Menu
        ShowMenu()

        try:
            Choice = int(input("\nChoose Data Execution's option: "))
            if Choice >= 0 and Choice <= 6:
                # Thoát Chương Trình
                if Choice == 0:
                    print ("Exit Program")
                    break
                
                # Hiện thị Data Frame
                elif Choice == 1:
                    print ("\nData Information")
                    Data_Frame.outputData()

                # Thêm bản ghi dữ liệu
                elif Choice == 2:
                    print ("\nAdd new data record")
                    while True:
                        new_data = input("Enter new comma-separated values' record: ").split(',')
                        if len(new_data) == len(Data_Frame.getSampleData()):
                            Data_Frame.addData(new_data)
                            break
                        else:
                            print ("Invalid field count. Enter data with correct field count.")

                # Cập nhật bản ghi
                elif Choice == 3:
                    print ("\nUpdate data record")
                    while True:
                        Updated_Index = input("Input updated data's index: ")
                        if Updated_Index.isdigit():
                            Updated_Index = int(Updated_Index)
                            if 0 < Updated_Index < len(Data_Frame.getData()):
                                break
                            else:
                                print ("\nInvalid input. Please try again")
                        else:
                            print ("\nInvalid input. Please enter a number.")
                    while True:
                        Updated_Data = input("Enter new comma-separated values' record: ").split(',')
                        if len(Updated_Data) == len(Data_Frame.getSampleData()):
                            Data_Frame.updateData(Updated_Index, Updated_Data)
                            break
                        else:
                            print ("Invalid field count. Please enter data with correct field count.")

                # Xóa bản ghi
                elif Choice == 4:
                    print ("\nDelete data record")
                    while True:
                        Deleted_Index = input("Input deleted data's index: ")
                        if Deleted_Index.isdigit():
                            Deleted_Index = int(Deleted_Index)
                            if 0 < Deleted_Index < len(Data_Frame.getData()):
                                break
                            else:
                                print ("Invalid input. Please choose again")
                        else:
                            print ("Invalid input. Please enter a number.")
                    Data_Frame.deleteData(Deleted_Index)

                # Lưu bản ghi
                elif Choice == 5:
                    print ("\nSave data record")
                    Data_Frame.saveData()

                # Làm sạch dữ liệu
                elif Choice == 6:
                
                    # Đọc dữ liệu từ file
                    Cleaning_Data = dataCleaner(Data_File)
                    print ("\nClean data")

                    print ("       +-----------------------------------DATA CLEANING OPTION-----------------------------------+")
                    print ("       |                                     0. Exit Cleaning                                     |")
                    print ("       | 1. Statistics of data                          5. Delete Missing Data's Row              |")
                    print ("       | 2. Sort Data Columns                           6. Filling Missing Data's Field by Column |")
                    print ("       | 3. Get Data's Information by row index         7. Standardize Data                       |")
                    print ("       | 4. Search Specific Data in a Column            8. Delete Outliers                        |")
                    print ("       |__________________________________________________________________________________________|")


                    while True:
                        try:
                            Clean_Choosing = int(input("Choose Cleaning Data's option: "))
                            if Clean_Choosing >= 0 and Clean_Choosing < 9:

                                # Thoát
                                if Clean_Choosing == 0:
                                    break

                                # Thống kê từng dữ liệu từ file
                                elif Clean_Choosing == 1:
                                    Cleaning_Data.aggregateData()

                                # Sắp xếp cột dữ liệu
                                elif Clean_Choosing == 2:
                                    while True:
                                        try:
                                            col_index = int(input("Input the column that you want to sort: "))
                                            if 0 <= col_index < len(Data_Frame.getSampleData()):
                                                reverse = input("Sort in ascending order? (y/n): ").lower() == 'y'
                                                Cleaning_Data.sortData(col_index=col_index, reverse=reverse)
                                                break
                                            else:
                                                print ("\nInvalid Input. Please choose again.")
                                                continue
                                        except ValueError:
                                            print ("\nInvalid input. Please enter a number")

                                # Lấy dữ liệu đối tượng thông qua chỉ số dòng
                                elif Clean_Choosing == 3:
                                    while True:
                                        try:
                                            Get_Index = int(input("Enter row index: "))
                                            if 0 <= Get_Index < len(Data_Frame.getData()):
                                                print(Cleaning_Data.getDataByIndex(Get_Index))
                                                break
                                            else:
                                                print ("\nInvalid Input. Please choose again.")
                                                continue
                                        except ValueError:
                                            print ("\nInvalid Input. Please enter a number.")

                                # Tìm kiếm thông tin các đối tượng qua tên cột và keyword
                                elif Clean_Choosing == 4:
                                    colName = input("Enter Column Name: ")
                                    if colName in Cleaning_Data.data.columns:
                                        keyword = input("Enter keyword: ")
                                        Cleaning_Data.searchData(keyword, colName)
                                    else:
                                        print ("Invalid Column Name.")

                                # Xóa những dòng bị thiếu dữ liệu
                                elif Clean_Choosing == 5:
                                    Cleaning_Data.deleteMissingData()

                                # Điền giá trị vào ô trống qua từng qua cột
                                elif Clean_Choosing == 6:
                                    colName = input("Enter Column Name: ")
                                    if colName in Cleaning_Data.data.columns:
                                        value = input("Enter Filling Value: ")
                                        Cleaning_Data.fillMissingData(colName, value)
                                    else:
                                        print ("Invalid Column Name.")

                                # Chuẩn hóa dữ liệu
                                elif Clean_Choosing == 7:
                                    Cleaning_Data.cleanCategoryData('Gender', ['male', 'female', 'other'])
                                    Cleaning_Data.cleanCategoryData('School_Type', ['public', 'private'])
                                    Cleaning_Data.cleanCategoryData('Parental_Education_Level', ['high school', 'college', 'postgraduate'])

                                # Xóa những giá trị ngoại lai
                                elif Clean_Choosing == 8:
                                    Cleaning_Data.deleteOutliers()

                                # Lưu dữ liệu đã được xử lý vào file khác
                                Cleaning_Data.data.to_csv(outfileDataCleaned, index=False)
                                print("Data is saved in new CSV file.")
                            else:
                                print ("\nInvalid input. Please choose again")
                                continue
                        except ValueError:
                            print ("\nInvalid input. Please enter a number")
            else:
                print ("\nInvalid input. Please choose again")
                continue
        except ValueError:
            print ("\nInvalid input. Please enter a number")

if __name__ == "__main__":
    main()
