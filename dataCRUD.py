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
    
    def outputData(self):
        # <In dữ liệu dưới dạng DataFrame của pandas>
        if self.data:
            print(pd.DataFrame(self.data))
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
                print("Dữ liệu không hợp lệ với số cột!")
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

    