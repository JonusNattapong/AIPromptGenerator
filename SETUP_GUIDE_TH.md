# AI Prompt Generator & Optimizer - คู่มือการติดตั้ง

คู่มือนี้จะอธิบายวิธีการติดตั้งและใช้งาน AI Prompt Generator & Optimizer ซึ่งเป็นเครื่องมือสำหรับสร้างและปรับแต่งคำถามหรือ prompt สำหรับ AI โมเดลต่างๆ เช่น ChatGPT, Claude, Gemini และอื่นๆ

## ขั้นตอนการติดตั้ง

### วิธีที่ 1: ใช้ Docker

1. ติดตั้ง Docker และ Docker Compose บนเครื่องของคุณ
   - สำหรับ Windows/Mac: ติดตั้ง Docker Desktop
   - สำหรับ Linux: ติดตั้ง Docker Engine และ Docker Compose

2. ดาวน์โหลดหรือโคลนโปรเจคนี้
   ```
   git clone https://github.com/JonusNattapong/ai-prompt-optimizer.git
   cd ai-prompt-optimizer
   ```

3. สร้างและเริ่มต้นคอนเทนเนอร์
   ```
   docker-compose up -d
   ```

4. เข้าใช้งานแอพพลิเคชันที่ http://localhost:8000

### วิธีที่ 2: ติดตั้งโดยตรงด้วย Python

1. ติดตั้ง Python 3.8 หรือใหม่กว่า

2. ดาวน์โหลดหรือโคลนโปรเจคนี้
   ```
   git clone https://github.com/JonusNattapong/ai-prompt-optimizer.git
   cd ai-prompt-optimizer
   ```

3. สร้าง virtual environment (แนะนำ)
   ```
   python -m venv venv
   
   # สำหรับ Windows
   venv\Scripts\activate
   
   # สำหรับ macOS/Linux
   source venv/bin/activate
   ```

4. ติดตั้งไลบรารี่ที่จำเป็น
   ```
   pip install -r requirements.txt
   ```

5. ดาวน์โหลด spaCy model
   ```
   python -m spacy download en_core_web_sm
   ```

6. สร้างโครงสร้างไดเรกทอรีและไฟล์ข้อมูลเริ่มต้น
   ```
   python create_folders.py
   ```

7. เริ่มต้นเซิร์ฟเวอร์
   ```
   uvicorn main:app --reload
   ```

8. เข้าใช้งานแอพพลิเคชันที่ http://localhost:8000

## การใช้งาน

### สร้าง Prompt ใหม่

1. ไปที่แท็บ "Generate"
2. กรอกเป้าหมายที่คุณต้องการให้ AI ช่วยเหลือ
3. เลือก AI โมเดลที่คุณต้องการใช้งาน
4. เลือกรูปแบบ (Style) ของ prompt ที่ต้องการ
5. เพิ่มบริบทหรือข้อมูลเพิ่มเติม (ถ้ามี)
6. เลือกตัวเลือกรูปแบบ (Format Options) ตามต้องการ
7. คลิก "Generate Prompt"
8. คุณสามารถคัดลอก บันทึก หรือทดสอบ prompt ที่สร้างได้

### ปรับแต่ง Prompt ที่มีอยู่แล้ว

1. ไปที่แท็บ "Optimize"
2. วาง prompt ที่คุณมีอยู่แล้วลงในช่อง
3. เลือก AI โมเดลที่คุณต้องการใช้งาน
4. เลือกระดับการปรับแต่ง (Optimization Level)
5. คลิก "Optimize Prompt"
6. คุณจะได้รับ prompt ที่ปรับแต่งแล้วพร้อมคำแนะนำในการปรับปรุง

### ทดสอบ Prompt

1. ไปที่แท็บ "Test"
2. วาง prompt ที่คุณต้องการทดสอบ
3. เลือกโมเดลที่ต้องการใช้ทดสอบ
4. คลิก "Run Test"
5. รอสักครู่ ระบบจะแสดงผลตอบกลับจาก AI

### บันทึกและจัดการ Prompt

1. คุณสามารถบันทึก prompt ที่สร้างหรือปรับแต่งแล้ว
2. prompt ที่บันทึกจะปรากฏในแท็บ "Library"
3. คุณสามารถค้นหา กรอง ใช้งาน หรือลบ prompt ในไลบรารี่ได้

## หมายเหตุเกี่ยวกับการใช้โมเดล Hugging Face

ระบบนี้ใช้โมเดล AI จาก Hugging Face สำหรับการทดสอบ prompt โดยตรง ซึ่งมีข้อควรระวังดังนี้:

1. โมเดลขนาดใหญ่ต้องการหน่วยความจำและการประมวลผลสูง แนะนำให้ใช้เครื่องที่มี GPU หรือเลือกใช้โมเดลขนาดเล็กกว่า
2. การโหลดโมเดลครั้งแรกอาจใช้เวลานาน
3. โมเดลบนระบบเป็นเพียงการจำลองการทำงานของ AI แพลตฟอร์มต่างๆ ผลลัพธ์อาจแตกต่างจากการใช้งานบนแพลตฟอร์มจริง

สำหรับการใช้งานจริงกับ ChatGPT, Claude หรือ Gemini คุณสามารถคัดลอก prompt ที่สร้างและนำไปใช้กับแพลตฟอร์มเหล่านั้นโดยตรง

## การปรับแต่งเพิ่มเติม

คุณสามารถปรับแต่งระบบเพิ่มเติมได้โดย:

1. เพิ่มโมเดล AI ใหม่ในไฟล์ `models.py` 
2. เพิ่มเทมเพลต prompt ในไฟล์ `data/prompt_templates.json`
3. เพิ่มแนวทางปฏิบัติที่ดีสำหรับแต่ละโมเดลในไฟล์ `data/model_best_practices.json`
4. ปรับแต่ง UI ในไฟล์ HTML, CSS และ JavaScript