import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings 
warnings.simplefilter(action='ignore', category=FutureWarning) #bỏ qua các dòng warning

file_path = 'cleaned_StudentPerformanceFactors.csv'

# Đọc dữ liệu vào DataFrame
data = pd.read_csv(file_path)

# Đặt kiểu hiển thị cho các biểu đồ
sns.set(style="whitegrid")


# 1. Histogram - Phân phối điểm thi
plt.figure(figsize=(10, 6))
sns.histplot(data['Exam_Score'], kde=True, bins=30, color='skyblue')
plt.title("Distribution of Exam Scores")
plt.xlabel("Exam Score")
plt.ylabel("Frequency")
plt.show()

# 2. Boxplot - Điểm thi theo mức độ tham gia của phụ huynh
plt.figure(figsize=(10, 6))
sns.boxplot(x='Parental_Involvement', y='Exam_Score', data=data, palette='pastel')
plt.title("Exam Score by Parental Involvement Level")
plt.xlabel("Parental Involvement")
plt.ylabel("Exam Score")
plt.show()

# 3. Scatter Plot - Số giờ học và Điểm thi
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Hours_Studied', y='Exam_Score', data=data, hue='Gender', palette='viridis', s=60)
plt.title("Hours Studied vs Exam Score")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.show()

# 4. Violin Plot - Điểm thi theo thu nhập gia đình
plt.figure(figsize=(10, 6))
sns.violinplot(x='Family_Income', y='Exam_Score', data=data, palette='muted')
plt.title("Exam Score by Family Income Level")
plt.xlabel("Family Income Level")
plt.ylabel("Exam Score")
plt.show()

# 5. Bar Chart - Mức độ truy cập Internet và Điểm thi trung bình
plt.figure(figsize=(10, 6))
internet_avg_score = data.groupby('Internet_Access')['Exam_Score'].mean().reset_index()
sns.barplot(x='Internet_Access', y='Exam_Score', data=internet_avg_score, palette='coolwarm')
plt.title("Average Exam Score by Internet Access")
plt.xlabel("Internet Access")
plt.ylabel("Average Exam Score")
plt.show()

# 6. Stacked Bar Chart - Hoạt động ngoại khóa và Tỷ lệ học sinh tham gia

extra_gender = data.groupby(['Extracurricular_Activities', 'Gender']).size().unstack()
extra_gender.plot(kind='bar', stacked=True, color=['#3498db', '#e74c3c'], figsize=(10, 6))
plt.title("Participation in Extracurricular Activities by Gender")
plt.xlabel("Extracurricular Activities")
plt.ylabel("Count")
plt.legend(title="Gender")
plt.show()

# 7. Pie Chart - Phân phối loại trường học
plt.figure(figsize=(8, 8))
school_type_counts = data['School_Type'].value_counts()
plt.pie(school_type_counts, labels=school_type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("Distribution of School Type")
plt.show()

# 8. Correlation Heatmap - Ma trận tương quan các biến số học tập
plt.figure(figsize=(12, 8))
correlation_matrix = data.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Numeric Study Factors")
plt.show()

# 9. Line Plot - Điểm thi trung bình theo mức chất lượng giáo viên
plt.figure(figsize=(10, 6))
teacher_quality_avg_score = data.groupby('Teacher_Quality')['Exam_Score'].mean().reset_index().sort_values(by='Teacher_Quality')
sns.lineplot(x='Teacher_Quality', y='Exam_Score', data=teacher_quality_avg_score, marker='o', color='teal')
plt.title("Average Exam Score by Teacher Quality")
plt.xlabel("Teacher Quality")
plt.ylabel("Average Exam Score")
plt.show()

# 10. Bar Chart - Điểm thi trung bình theo trình độ học vấn của phụ huynh
plt.figure(figsize=(10, 6))
parental_education_avg_score = data.groupby('Parental_Education_Level')['Exam_Score'].mean().reset_index()
sns.barplot(x='Parental_Education_Level', y='Exam_Score', data=parental_education_avg_score, palette='viridis')
plt.title("Average Exam Score by Parental Education Level")
plt.xlabel("Parental Education Level")
plt.ylabel("Average Exam Score")
plt.xticks(rotation=45)
plt.show()
