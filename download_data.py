import wfdb
import os

# نام دیتابیس در وب‌سایت PhysioNet
db_name = 'mitdb'

# پوشه‌ای که می‌خواهید داده‌ها در آن ذخیره شوند
# این پوشه در کنار اسکریپت شما ساخته خواهد شد
save_directory = 'mit-bih-arrhythmia-database-1.0.0'

print(f"Starting download of the {db_name} database...")
print(f"Data will be saved in the '{save_directory}' directory.")

try:
    # این تابع کل دیتابیس را به همراه تمام فایل‌های لازم دانلود می‌کند
    wfdb.dl_database(db_name, dl_dir=save_directory)
    print("\nDatabase downloaded successfully!")

    # بررسی محتویات پوشه برای اطمینان
    files_in_dir = os.listdir(save_directory)
    print(f"Total files and directories downloaded: {len(files_in_dir)}")
    print("A few example files:", files_in_dir[:5])

except Exception as e:
    print(f"\nAn error occurred during download: {e}")
    print("Please check your internet connection and permissions.")