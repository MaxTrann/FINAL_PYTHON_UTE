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
        # <Thống kê giá trị xuất hiện trong từng cột của DataFrame>
        print("Thống kê các giá trị có trong file:")
        for col in self.data.columns:
            print(f"\nThông tin về cột {col}': ")
            print(self.data[col].value_counts())
            
    def sortData(self, col_index=0, reverse=False):
        # <Sắp xếp dữ liệu theo một cột được chỉ định>
        try:
            col_name = self.data.columns[col_index]
            self.data = self.data.sort_values(by=col_name, ascending=reverse)
            print("Dữ liệu đã được sắp xếp!")
        except IndexError:
            print("Chỉ số cột không hợp lệ!")
    
    def getDataByIndex(self, idx):
        # <Lấy dữ liệu thông qua chỉ số dòng>
        if 0 <= idx <= len(self.data):
            return self.data.iloc[idx - 1] # ở đây lấy idx - 1 bởi vì người dùng sẽ nhìn vào file csv để thao tác mà dòng 0 chứa biến dữ liệu, nên record bắt đầu ở dòng 1 tuy nhiên theo cách thức hoạt động của list bắt đầu từ 0 nên trừ đi 1 
        else:
            print("Vị trí không hợp lệ!")
            return None
    
    def searchData(self, keyword, colName):
        # <Tìm kiếm dữ liệu trong một cột dựa trên từ khóa>
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
        # <Hàm để loại bỏ những dòng bị thiếu dữ liệu NaN>
        self.data = self.data.dropna(axis=0)
    
    def fillMissingData(self, colName, value):
        # <Điền giá trị cụ thể vào các ô trống trong một cột. Cho biết được số dòng còn thiếu trong cột đó>
        if colName in self.data.columns:
            missingCnt = self.data[colName].isna().sum() # đếm số lượng cột bị thiếu
            if missingCnt > 0:
                self.data[colName].fillna(value, inplace = True)
                print(f"Thêm giá trị {value} vào {colName} thành công!")
                print(f"Số lượng giá trị đã được điền thêm: {missingCnt}")
            else:
                print(f"Cột {colName} không có giá trị bị thiếu")
        else:
            print("Tên cột không hợp lệ")
    
    def standardizeCategoryData(self, colName):
        # <Chuẩn hóa dữ liệu trong một cột>
        self.data[colName] = self.data[colName].str.capitalize()
    
    
    def deleteOutliers(self):
        # <Loại bỏ các giá trị ngoại lai dựa trên những nguyên tắc đã được định sẵn>
        validGenders = ['Male', 'Female', 'Other']
        self.data = self.data[self.data['Gender'].isin(validGenders)] # Những cú pháp hợp lệ của gender   
        self.data = self.data[(self.data['Exam_Score'] <= 100) & (self.data['Exam_Score'] >= 0)] # Xử lí trường hợp điểm số
