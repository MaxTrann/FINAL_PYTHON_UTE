from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, simpledialog, Toplevel, Scrollbar, Frame, filedialog, ttk, END, WORD, BOTH, DISABLED
from dataCRUD import dataProcessing
from dataCleaning import *
from tkinter.scrolledtext import ScrolledText
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "GUI" / "build" / "assets" / "frame0"


def relative_to_assets(path: str) -> Path:
    """
    Trả về đường dẫn tương đối tới thư mục assets.

    :param path: Đường dẫn tương đối từ thư mục assets.
    :return: Đường dẫn đầy đủ tới file trong thư mục assets.
    """
    return ASSETS_PATH / Path(path)


class DataApp:
    def __init__(self, root):
        """
        Khởi tạo ứng dụng DataApp với cửa sổ chính.

        :param root: Cửa sổ chính của ứng dụng.
        """
        self.root = root
        self.root.geometry("962x557")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.data_file = 'StudentPerformanceFactors.csv'
        self.cleaned_file = "cleaned_StudentPerformanceFactors.csv"

        self.data_frame = dataProcessing(self.data_file)
        self.setup_ui()

    def setup_ui(self):
        """
        Thiết lập giao diện người dùng cho ứng dụng.
        """
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
    def run_visualization(self):
        """Chạy script visualization.py để hiển thị các biểu đồ."""
        try:
            subprocess.run(["python", "visualization.py"], check=True)
            messagebox.showinfo("Success", "Visualization script executed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_buttons(self, canvas):
        """Tạo các nút chức năng trong ứng dụng."""
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
                canvas,
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat"
            )
            button.image = button_image
            button.place(x=x, y=y, width=width, height=height)

        # Thêm nút chạy visualization ở góc trên phải
        visualization_button = ttk.Button(canvas, text="Run Visualization", command=self.run_visualization)
        visualization_button.place(relx=1.0, x=-10, y=10, anchor='ne')

    

    def display_data(self):
        """Hiển thị dữ liệu trong một cửa sổ mới."""
        try:
            data = self.data_frame.getData()
            if data:
                # Tạo cửa sổ con
                top = Toplevel(self.root)
                top.title("Data Viewer")
                top.geometry("900x600")
                top.configure(bg="#f4f4f4")  # Màu nền dịu nhẹ

                # Số dòng mỗi trang
                rows_per_page = 20
                total_pages = (len(data) + rows_per_page - 1) // rows_per_page  # Tính số trang
                current_page = 1

                # Thêm Frame quản lý Treeview widget và Scrollbars
                frame = Frame(top, bg="#f4f4f4", pady=10, padx=10)
                frame.pack(fill="both", expand=True)

                # Tạo Treeview
                tree = ttk.Treeview(frame, columns=["#"] + [f"Column {i+1}" for i in range(len(data[0]))], show="headings")
                tree.grid(row=0, column=0, sticky="nsew")

                # Cấu hình các cột
                tree.heading("#", text="No.")
                for i in range(len(data[0])):
                    tree.heading(i+1, text=f"Column {i+1}", anchor="center")
                    tree.column(i+1, anchor="center", width=120)  # Căn giữa và thiết lập độ rộng cột

                # Tạo Scrollbars
                scroll_y = Scrollbar(frame, orient="vertical", command=tree.yview)
                scroll_y.grid(row=0, column=1, sticky="ns")

                scroll_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
                scroll_x.grid(row=1, column=0, sticky="ew")

                # Gắn Scrollbars với Treeview
                tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

                # Cấu hình lưới trong Frame
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # Thêm các dữ liệu vào Treeview
                def display_page(page):
                    for i in tree.get_children():
                        tree.delete(i)  # Xóa dữ liệu cũ
                    start_index = (page - 1) * rows_per_page
                    end_index = start_index + rows_per_page
                    page_data = data[start_index:end_index]

                    for i, row in enumerate(page_data, start=start_index+1):
                        tree.insert("", "end", values=[i] + row)

                # Hàm xử lý khi chuyển trang
                def next_page():
                    nonlocal current_page
                    if current_page < total_pages:
                        current_page += 1
                        display_page(current_page)

                def prev_page():
                    nonlocal current_page
                    if current_page > 1:
                        current_page -= 1
                        display_page(current_page)

                # Thêm các nút chuyển trang
                button_frame = Frame(top, bg="#f4f4f4")
                button_frame.pack(fill="x", pady=10)

                prev_button = Button(button_frame, text="Previous", command=prev_page, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
                prev_button.pack(side="left", padx=5)

                next_button = Button(button_frame, text="Next", command=next_page, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
                next_button.pack(side="right", padx=5)

                # Thêm nút Export
                def export_to_file():
                    try:
                        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
                        if file_path:
                            with open(file_path, "w") as file:
                                for row in data:
                                    file.write("\t".join(map(str, row)) + "\n")
                            messagebox.showinfo("Success", "Data exported successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export data: {e}")

                export_button = Button(button_frame, text="Export to File", command=export_to_file, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
                export_button.pack(side="left", padx=5)

                # Hiển thị trang đầu tiên
                display_page(current_page)

            else:
                messagebox.showwarning("No Data", "No data available to display.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


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

    def save_cleaned_data(self, data):
        """
        Lưu dữ liệu đã làm sạch vào một tệp.

        :param data: Dữ liệu đã làm sạch để lưu.
        """
        try:
            data.to_csv(self.cleaned_file, index=False)
            print(f"Data has been automatically saved to {self.cleaned_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def show_data_in_window(self, title, data):
        """
        Hiển thị dữ liệu trong một cửa sổ mới.

        :param title: Tiêu đề của cửa sổ.
        :param data: Dữ liệu để hiển thị.
        """
        window = Toplevel()
        window.title(title)
        text_area = ScrolledText(window, wrap=WORD, width=100, height=30)
        text_area.pack(expand=True, fill=BOTH)
        text_area.insert(END, data)
        text_area.config(state=DISABLED)

    def data_statistics(self):
        """Hiển thị thống kê dữ liệu trong cửa sổ mới."""
        try:
            cleaner = dataCleaner(self.data_file)
            # Gọi hàm aggregateData và lấy kết quả từ stdout
            import io
            import sys

            # Tạo một StringIO object để lưu trữ kết quả in ra
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            # Gọi hàm aggregateData
            cleaner.aggregateData()

            # Lấy kết quả từ buffer
            sys.stdout = old_stdout
            statistics = buffer.getvalue()

            # Hiển thị kết quả trong cửa sổ mới
            self.show_data_in_window("Data Statistics", statistics)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def sort_data(self):
        """Sắp xếp dữ liệu theo một cột cụ thể và cập nhật hiển thị."""
        try:
            col_index = int(simpledialog.askstring("Input", "Enter column index to sort:"))
            reverse = simpledialog.askstring("Input", "Sort in ascending order? (y/n):").lower() == 'y'
            cleaner = dataCleaner(self.data_file)
            cleaner.sortData(col_index=col_index, reverse=reverse)
            self.save_cleaned_data(cleaner.data)
            self.show_data_in_window("Sorted Data", cleaner.data.to_string())
        except ValueError:
            messagebox.showerror("Error", "Invalid column index.")

    def get_data_by_index(self):
        """Lấy dữ liệu từ một dòng cụ thể và hiển thị trong cửa sổ."""
        try:
            index = int(simpledialog.askstring("Input", "Enter row index:"))
            cleaner = dataCleaner(self.data_file)
            data = cleaner.getDataByIndex(index)
            messagebox.showinfo("Data by Index", f"{data}")
        except ValueError:
            messagebox.showerror("Error", "Invalid index.")

    def search_data(self):
        """
        Tìm kiếm dữ liệu và hiển thị kết quả giống như trong terminal.
        """
        try:
            cleaner = dataCleaner(self.data_file)
            import io
            import sys

            while True:
                # Yêu cầu người dùng nhập tên cột
                col_name = simpledialog.askstring("Input", "Enter column name:")
                if col_name is None:  # Nếu người dùng nhấn Cancel
                    break

                if col_name in cleaner.data.columns:
                    # Yêu cầu người dùng nhập từ khóa tìm kiếm
                    keyword = simpledialog.askstring("Input", "Enter keyword to search:")
                    if keyword is None:  # Nếu người dùng nhấn Cancel
                        break

                    # Chuyển hướng đầu ra để bắt lại thông tin in ra
                    output = io.StringIO()
                    sys.stdout = output  # Đổi hướng in ra thành StringIO

                    # Gọi hàm searchData và in kết quả ra "output"
                    cleaner.searchData(keyword, col_name)

                    # Khôi phục lại đầu ra chuẩn
                    sys.stdout = sys.__stdout__

                    # Lấy chuỗi kết quả tìm kiếm từ output
                    result_string = output.getvalue()

                    # Kiểm tra nếu có kết quả in ra
                    if result_string.strip():
                        # Hiển thị kết quả trong cửa sổ cuộn
                        self.show_data_in_window("Search Results", result_string)
                    else:
                        # Nếu không có kết quả, hiển thị thông báo
                        messagebox.showinfo("Search Results", "No matching records found.")
                    break
                else:
                    # Thông báo nếu tên cột không hợp lệ
                    messagebox.showwarning("Invalid Column", "Invalid Column Name. Please try again.")

        except Exception as e:
            # Hiển thị thông báo lỗi nếu có vấn đề xảy ra
            messagebox.showerror("Error", f"An error occurred: {e}")




    def delete_missing_data(self):
        """Xoá các dòng chứa dữ liệu thiếu và cập nhật hiển thị."""
        cleaner = dataCleaner(self.data_file)
        cleaner.deleteMissingData()
        self.save_cleaned_data(cleaner.data)
        self.show_data_in_window("Data After Deleting Missing Values", cleaner.data.to_string())

    def fill_missing_data(self):
        """Điền giá trị vào các ô dữ liệu thiếu và cập nhật hiển thị."""
        try:
            cleaner = dataCleaner(self.data_file)
            while True:
                col_name = simpledialog.askstring("Input", "Enter column name to fill:")
                if col_name is None:
                    break
                if col_name in cleaner.data.columns:
                    value = simpledialog.askstring("Input", "Enter value to fill missing data:")
                    if value is None:
                        break
                    cleaner.fillMissingData(col_name, value)
                    self.save_cleaned_data(cleaner.data)
                    self.show_data_in_window("Data After Filling Missing Values", cleaner.data.to_string())
                    break
                else:
                    messagebox.showwarning("Invalid Column", "Invalid Column Name. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def standardize_data(self):
        """Chuẩn hóa dữ liệu và cập nhật hiển thị."""
        try:
            cleaner = dataCleaner(self.data_file)
            while True:
                standardized_col = simpledialog.askstring("Input", "Input column you want to standardize:")
                if standardized_col is None:
                    break
                if standardized_col in cleaner.data.columns:
                    valid_list = simpledialog.askstring("Input", "Enter valid values separated by comma:")
                    if valid_list is None:
                        break
                    valid_list = valid_list.split(',')
                    cleaner.cleanCategoryData(standardized_col, valid_list)
                    self.show_data_in_window("Standardized Data", cleaner.data.to_string())
                else:
                    messagebox.showwarning("Invalid Column", "Invalid Column Name. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_outliers(self):
        """
        Xóa các giá trị ngoại lai khỏi dữ liệu và cập nhật hiển thị.
        """
        cleaner = dataCleaner(self.data_file)
        cleaner.deleteOutliers()
        self.save_cleaned_data(cleaner.data)
        self.show_data_in_window("Dữ liệu sau khi xóa ngoại lai", cleaner.data.to_string())


if __name__ == "__main__":
    window = Tk()
    app = DataApp(window)
    window.mainloop()
