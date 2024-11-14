import pandas as pd

class dataCleaner:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = self.loadData()
    
    def loadData(self):
        # <Đọc dữ liệu từ file csv và trả về một DataFrame>
        try:
            return pd.read_csv(self.filePath)
        except Exception as e:
            print(f"File {self.filePath} lỗi {e}")
            return pd.DataFrame()
    
    def aggregateData(self):
        # <Thống kê dữ liệu của file>
        print("Thống kê các giá trị có trong file:")
        for col in self.data.columns:
            print(f"\nThông tin về cột {col}': ")
            print(self.data[col].value_counts())
            
    def sortData(self, col_index=0, reverse=False):
        try:
            col_name = self.data.columns[col_index]
            self.data = self.data.sort_values(by=col_name, ascending=reverse)
            print("Dữ liệu đã được sắp xếp!")
        except IndexError:
            print("Chỉ số cột không hợp lệ!")
    
    def getDataByIndex(self, idx):
        # <Lấy dữ liệu thông qua chỉ số dòng>
        if 0 <= idx <= len(self.data):
            return self.data[idx]
        else:
            print("Vị trí không hợp lệ!")
            return None
    
    def searchData(self, keyword, colName):
        # <Tìm kiếm dữ liệu thông qua keyword, và tên cột>
        if colName in self.data.columns:
            ans = self.data[self.data[colName].astype(str).str.contains(keyword,case=False,na=False)]
            if not ans.empty:
                print("Kết quả tìm kiếm: ")
                print(ans)
            else:
                print("Không tìm thấy kết quả!")
        else:
            print(f"{colName} không có trong dữ liệu!") 
    
    
    def deleteMissingData(self):
        # <Hàm để loại bỏ những dòng bị thiếu dữ liệu NULL (NaN)>
        self.data = self.data.dropna(axis=0)
    
    def fillMissingData(self, colName, value):
        # <Điền giá trị vào ô trống trong một cột>
        if colName in self.data.columns:
            self.data[colName].fillna(value)
            print(f"Thêm giá trị {value} vào {colName} thành công!")
        else:
            print("Tên cột không hợp lệ")
    
    def cleanCategoriData(self, colName, validValues):
        # <Chuẩn hóa dữ liệu chữ Femal thì femal được; Public thì public được>
        self.data[colName] = self.data[colName].str.lower()
        self.data = self.data[self.data[colName].isin(validValues)]
    
    
    def deleteOutliers(self):
        # <Xử lí các số liệu ngoại lai>
        validGenders = ['Male', 'Female', 'Other']
        self.data = self.data[self.data['Gender'].isin(validGenders)] # Những cú pháp hợp lệ của gender   
        self.data = self.data[(self.data['Exam_Score'] <= 100) & (self.data['Exam_Score'] >= 0)] # Xử lí trường hợp điểm số
        
    
def main():
    cleaner = dataCleaner("StudentPerformanceFactors.csv")

    # Chuẩn hóa cột phân loại
    cleaner.cleanCategoricalData('Gender', ['male', 'female', 'other'])
    cleaner.cleanCategoricalData('School_Type', ['public', 'private'])
    

    
