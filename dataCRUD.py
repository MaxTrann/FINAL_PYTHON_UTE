import csv
import pandas as pd 

class dataProcessing:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = self.getData() # Lấy dữ liệu từ file csv
        
    def getData(self):
        # <Tải dữ liệu từ file csv và trả về một list cái dòng record>
        data = [] # tạo một list để chứa các dòng dữ liệu 
        try:
            with open(self.filePath, mode = 'r', newline='', encoding='utf-8') as filecsv:
                readData = csv.reader(filecsv)
                data = list(readData) # Dùng hàm list sẽ tối ưu khi duyệt for đối với data lớn
        except Exception as e:
            print(f"File {self.filePath} lỗi {e}!")
        return data
    
    def outputData(self, records_per_page = 1000):
        # <In dữ liệu dưới dạng DataFrame của pandas>
        if self.data:
            """
                In dữ liệu dưới dạng DataFrame để phân trang. records_per_page: Số lượng dòng mỗi trang
            """
            df = pd.DataFrame(self.data)
            
            # Tính số trang
            total_records = len(df)
            total_pages = (total_records + records_per_page - 1) // records_per_page
            
            curr_page = 1
            while True:
                # Tính chỉ số dòng bắt đầu và kết thúc
                start_idx = (curr_page - 1) * records_per_page
                end_idx = min(start_idx + records_per_page, total_records)
                
                # Lấy dữ liệu cho trang
                data_page = df.iloc[start_idx:end_idx]
                
                print(f"Trang {curr_page}/{total_pages}:")
                print(data_page)
                
                if curr_page == total_pages:
                    print("Dữ liệu kết thúc!")
                    break
                
                # Yêu cầu của người dùng
                user_request = int(input("Nhập '1' để sang trang, '-1' để quay lại, hoặc '0' để thoát:"))
                if user_request == 1 and curr_page < total_pages:
                    curr_page += 1
                elif user_request == -1 and curr_page > 1:
                    curr_page -= 1
                elif user_request == 0:
                    print('Thoát!')
                    break
                else:
                    print("Nhập không hợp lệ!")   
        else:
            print("Dữ liệu trống hoặc chưa được tải!")
        
    def getSampleData(self):
        # <Trả về bản ghi đầu tiên của dữ liệu để lấy đó làm mẫu>
        return self.data[0] if self.data else []
    
    def addData(self, newData):
        # <Thêm record vào cho dữ liệu>
        if len(newData) == len(self.getSampleData()):
            self.data.append(newData)
            print("Dữ liệu đã được thêm!")
        else:
            print("Dữ liệu bị chưa chính xác hoặc có lỗi!")
        
    def updateData(self, index, newData):
        # <Cập nhật dữ liệu mới cho record>
        if index >= 0 and index < len(self.data):
            if len(newData) == len(self.data[index]):
                self.data[index] = newData
                print("Dữ liệu đã được cập nhật!")
            else:
                print("Dữ liệu không hợp lệ với số dòng!")
        else:
            print("Vị trí thêm không hợp lệ!")
            
    def deleteData(self, index):
        # <Xóa record>
        if index >= 0 and index < len(self.data):
            self.data.pop(index)
            print("Dữ liệu đã được xóa!")
        else:
            print("Vị trí xóa không hợp lệ!")
        
    def saveData(self):
        # <Lưu dữ liệu hiện tại vào csv file>
        try:
            with open(self.filePath, mode='w', newline='', encoding='utf-8') as filecsv:
                write = csv.writer(filecsv)
                write.writerows(self.data)
            print("Dữ liệu đã được lưu thành công!")
        except Exception as e:
            print(f"File đang gặp lỗi {e}")

    
