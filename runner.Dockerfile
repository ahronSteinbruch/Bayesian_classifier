# 1. התחל מתמונת בסיס רזה של פייתון
FROM python:3.9-slim

# 2. הגדר את תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# 3. העתק את קובץ הדרישות והתקן את הספריות
#    זה מבטיח ש-requests ו-pandas יהיו זמינים לסקריפט
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. העתק רק את הקבצים שה-runner צריך כדי לרוץ
COPY main.py .
COPY Intelligence_Selection.csv .

# 5. הגדר את הפקודה שתרוץ כשהקונטיינר יתחיל
CMD ["python", "main.py"]