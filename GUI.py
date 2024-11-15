from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, simpledialog, Toplevel
from dataCRUD import dataProcessing
from dataCleaning import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\LTPYTHON\FINAL_PYTHON_UTE\GUI\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("962x557")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.data_file = 'StudentPerformanceFactors.csv'
        self.cleaned_file = "cleaned_StudentPerformanceFactors.csv"

        self.data_frame = dataProcessing(self.data_file)
        self.setup_ui()

    def setup_ui(self):
        canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=557,
            width=962,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(0.0, 0.0, 962.0, 36.0, fill="#DFE1E5", outline="")
        canvas.create_text(
            372.0, 6.0,
            anchor="nw",
            text="Data Execution Options",
            fill="#0676F7",
            font=("Noto Sans", 18 * -1)
        )

        self.create_buttons(canvas)

        canvas.create_text(
            139.0, 529.0,
            anchor="nw",
            text="Trương Công Bình - Ninh Thị Mỹ Hạnh - Trần Lê Quốc Đại - Đoàn Quang Khôi - Nguyễn Thị Hoàng Kim",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

    def create_buttons(self, canvas):
        button_config = [
            ("button_2.png", self.display_data, 82.0, 83.0, 344.0, 100.0),
            ("button_7.png", self.add_record, 533.0, 83.0, 344.0, 100.0),
            ("button_6.png", self.update_record, 82.0, 229.0, 344.0, 100.0),
            ("button_5.png", self.delete_record, 533.0, 229.0, 344.0, 100.0),
            ("button_4.png", self.save_data, 82.0, 375.0, 344.0, 100.0),
            ("button_3.png", self.open_data_cleaning_options, 533.0, 375.0, 344.0, 100.0)
        ]

        for image, command, x, y, width, height in button_config:
            button_image = PhotoImage(file=relative_to_assets(image))
            button = Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat"
            )
            button.image = button_image
            button.place(x=x, y=y, width=width, height=height)

    def display_data(self):
        data = self.data_frame.getData()
        if data:
            display = "\n".join(map(str, data))
            messagebox.showinfo("Data Sheet", display)
        else:
            messagebox.showwarning("No Data", "No data available to display.")

    def add_record(self):
        new_data = simpledialog.askstring("Input", "Enter new comma-separated values' record:")
        if new_data:
            record = new_data.split(',')
            if len(record) == len(self.data_frame.getSampleData()):
                self.data_frame.addData(record)
                messagebox.showinfo("Success", "Record added successfully.")
            else:
                messagebox.showerror("Error", "Invalid field count.")

    def update_record(self):
        try:
            index = int(simpledialog.askstring("Input", "Enter the record index to update:"))
            updated_data = simpledialog.askstring("Input", "Enter new comma-separated values' record:")
            if updated_data:
                record = updated_data.split(',')
                if len(record) == len(self.data_frame.getSampleData()):
                    self.data_frame.updateData(index, record)
                    messagebox.showinfo("Success", "Record updated successfully.")
                else:
                    messagebox.showerror("Error", "Invalid field count.")
        except ValueError:
            messagebox.showerror("Error", "Invalid index.")

    def delete_record(self):
        try:
            index = int(simpledialog.askstring("Input", "Enter the record index to delete:"))
            self.data_frame.deleteData(index)
            messagebox.showinfo("Success", "Record deleted successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid index.")

    def save_data(self):
        self.data_frame.saveData()
        messagebox.showinfo("Success", "Data saved successfully.")

    # def clean_data_menu(self):
    #     # Cleaning data menu
    #     cleaning_window = Toplevel(self.root)
    #     cleaning_window.title("Data Cleaning Options")

    #     Button(cleaning_window, text="Statistics of Data", command=self.data_statistics).pack(pady=5)
    #     Button(cleaning_window, text="Sort Data Columns", command=self.sort_data).pack(pady=5)
    #     Button(cleaning_window, text="Get Data by Index", command=self.get_data_by_index).pack(pady=5)
    #     Button(cleaning_window, text="Search Specific Data in a Column", command=self.search_data).pack(pady=5)
    #     Button(cleaning_window, text="Delete Missing Data's Row", command=self.delete_missing_data).pack(pady=5)
    #     Button(cleaning_window, text="Fill Missing Data", command=self.fill_missing_data).pack(pady=5)
    #     Button(cleaning_window, text="Standardize Data", command=self.standardize_data).pack(pady=5)
    #     Button(cleaning_window, text="Delete Outliers", command=self.delete_outliers).pack(pady=5)
    def open_data_cleaning_options(self):
        # Tạo cửa sổ Toplevel
        data_cleaning_window = Toplevel()
        data_cleaning_window.geometry("970x539")
        data_cleaning_window.configure(bg="#FFFFFF")
        
        # Canvas trong Toplevel
        canvas = Canvas(
            data_cleaning_window,
            bg="#FFFFFF",
            height=539,
            width=970,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0, 0.0, 970.0, 36.0,
            fill="#DFE1E5",
            outline=""
        )
        canvas.create_text(
            381.0, 6.0,
            anchor="nw",
            text="Data Cleaning Options",
            fill="#0676F7",
            font=("Noto Sans", 18 * -1)
        )

        # Các nút trong Toplevel với các chức năng
        button_image_1 = PhotoImage(file=relative_to_assets("delete_missing_data_row.png"))
        Button(
            data_cleaning_window,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_missing_data,
            relief="flat"
        ).place(x=68.0, y=86.0, width=384.0, height=68.0)

        button_image_4 = PhotoImage(file=relative_to_assets("delete_outliers.png"))
        Button(
            data_cleaning_window,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_outliers,
            relief="flat"
        ).place(x=517.0, y=86.0, width=384.0, height=68.0)

        button_image_5 = PhotoImage(file=relative_to_assets("fill_missing_data.png"))
        Button(
            data_cleaning_window,
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.fill_missing_data,
            relief="flat"
        ).place(x=68.0, y=386.0, width=384.0, height=68.0)

        button_image_6 = PhotoImage(file=relative_to_assets("get_data_by_index.png"))
        Button(
            data_cleaning_window,
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.get_data_by_index,
            relief="flat"
        ).place(x=517.0, y=386.0, width=384.0, height=68.0)

        button_image_7 = PhotoImage(file=relative_to_assets("search_specific_data_in_a_column.png"))
        Button(
            data_cleaning_window,
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.search_data,
            relief="flat"
        ).place(x=68.0, y=286.0, width=384.0, height=69.0)

        button_image_8 = PhotoImage(file=relative_to_assets("sort_data_columns.png"))
        Button(
            data_cleaning_window,
            image=button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=self.sort_data,
            relief="flat"
        ).place(x=517.0, y=286.0, width=384.0, height=69.0)

        button_image_9 = PhotoImage(file=relative_to_assets("standarize_data.png"))
        Button(
            data_cleaning_window,
            image=button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=self.standardize_data,
            relief="flat"
        ).place(x=68.0, y=191.0, width=384.0, height=68.0)

        button_image_10 = PhotoImage(file=relative_to_assets("statistics_of_data.png"))
        Button(
            data_cleaning_window,
            image=button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=self.data_statistics,
            relief="flat"
        ).place(x=517.0, y=191.0, width=384.0, height=68.0)

        # Tạo phần ghi chú thông tin
        canvas.create_text(
            142.0, 504.0,
            anchor="nw",
            text="Trương Công Bình - Ninh Thị Mỹ Hạnh - Trần Lê Quốc Đại - Đoàn Quang Khôi - Nguyễn Thị Hoàng Kim",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        data_cleaning_window.resizable(False, False)
        data_cleaning_window.mainloop()

    def data_statistics(self):
        cleaner = dataCleaner(self.data_file)
        cleaner.aggregateData()

    def sort_data(self):
        try:
            col_index = int(simpledialog.askstring("Input", "Enter column index to sort:"))
            reverse = simpledialog.askstring("Input", "Sort in ascending order? (y/n):").lower() == 'y'
            cleaner = dataCleaner(self.data_file)
            cleaner.sortData(col_index=col_index, reverse=reverse)
        except ValueError:
            messagebox.showerror("Error", "Invalid column index.")

    def get_data_by_index(self):
        try:
            index = int(simpledialog.askstring("Input", "Enter row index:"))
            cleaner = dataCleaner(self.data_file)
            data = cleaner.getDataByIndex(index)
            messagebox.showinfo("Data by Index", f"{data}")
        except ValueError:
            messagebox.showerror("Error", "Invalid index.")

    def search_data(self):
        col_name = simpledialog.askstring("Input", "Enter column name:")
        keyword = simpledialog.askstring("Input", "Enter keyword to search:")
        cleaner = dataCleaner(self.data_file)
        cleaner.searchData(keyword, col_name)

    def delete_missing_data(self):
        cleaner = dataCleaner(self.data_file)
        cleaner.deleteMissingData()

    def fill_missing_data(self):
        col_name = simpledialog.askstring("Input", "Enter column name to fill:")
        value = simpledialog.askstring("Input", "Enter value to fill missing data:")
        cleaner = dataCleaner(self.data_file)
        cleaner.fillMissingData(col_name, value)

    def standardize_data(self):
        cleaner = dataCleaner(self.data_file)
        cleaner.cleanCategoryData('Gender', ['male', 'female', 'other'])
        cleaner.cleanCategoryData('School_Type', ['public', 'private'])
        cleaner.cleanCategoryData('Parental_Education_Level', ['high school', 'college', 'postgraduate'])

    def delete_outliers(self):
        cleaner = dataCleaner(self.data_file)
        cleaner.deleteOutliers()


if __name__ == "__main__":
    window = Tk()
    app = DataApp(window)
    window.mainloop()
