นางสาวปุณยภา จรรยากรณ์ รหัส 68114540405
### รายละเอียดเกี่ยวกับเกม Rocket Evolution

เกม **Rocket Evolution** เป็นเกมยิงยานอวกาศ (Space Shooter) ที่พัฒนาโดยใช้ภาษา Python และไลบรารี Pygame ผู้เล่นจะควบคุมยานอวกาศเพื่อต่อสู้กับศัตรูต่างๆ รวมถึงดาวตก (meteors) และบอส โดยมีเป้าหมายในการเก็บคะแนนให้สูงสุดผ่านการยิงศัตรูและเก็บไอเท็มพาวเวอร์อัพ

#### วิธีการเล่น
1. **วัตถุประสงค์หลัก**: ยิงศัตรู (enemies) เพื่อเก็บคะแนน (10 คะแนนต่อศัตรูปกติ, 500 คะแนนสำหรับบอส) หลีกเลี่ยงการชนกับศัตรู ดาวตก หรือกระสุนศัตรูเพื่อรักษาชีวิต (เริ่มต้น 100 HP)
2. **องค์ประกอบหลัก**:
   - **ผู้เล่น (Player)**: ยานอวกาศสีน้ำเงินที่สามารถขยับและยิงกระสุน
   - **ศัตรู (Enemies)**: ยานศัตรูสีต่างๆ (แดง, น้ำเงิน, เขียว, ส้ม, ดำ) และ UFO ที่ยิงกระสุนตามทาง (homing bullets)
   - **บอส (Boss)**: ปรากฏเมื่อคะแนนถึง 100 คะแนน มีเลือด 500 HP ยิงกระสุนตามทางและมีกองทัพปกป้อง
   - **ดาวตก (Meteors)**: ดาวตกขนาดต่างๆ ที่ตกลงมา สีน้ำตาลและเทา หากชนจะเสียเลือด 20 HP
   - **ไอเท็มพาวเวอร์อัพ (Power-ups)**: แผงสีต่างๆ ที่ตกลงมา เช่น
     - **โล่ทอง (Gold Shield)**: ป้องกันความเสียหาย 7 วินาที
     - **เพิ่มความเร็ว (Speed Boost)**: เพิ่มความเร็วการขยับ 5 วินาที
     - **ดาว (Stars)**: เก็บเพื่อเลเวลอัพ (Bronze/Silver/Gold) และเข้าสู่โหมด Hyper (เพิ่มความเสียหายและความเร็ว)
     - **ฟื้นเลือด (Green Pill)**: ฟื้นเลือด 20 HP
3. **ระบบเลเวลอัพ**: เก็บดาวเพื่อเข้าสู่โหมด Hyper (30 วินาที) ซึ่งเพิ่มความเสียหายและความเร็วการยิง
4. **การจบเกม**: เมื่อเลือดหมดหรือชนสิ่งกีดขวาง จะแพ้เกม สามารถกด R เพื่อเริ่มใหม่หรือ Q เพื่อออก

#### รายการควบคุม
- **ขยับยาน**: 
  - ลูกศรซ้าย/ขวา หรือ A/D สำหรับขยับซ้าย/ขวา
  - ลูกศรขึ้น/ลง หรือ W/S สำหรับขยับขึ้น/ลง
- **ยิงกระสุน**: Spacebar (กดค้างเพื่อยิงต่อเนื่อง)
- **เริ่มใหม่**: R (หลังแพ้)
- **ออกเกม**: Q (หลังแพ้)

#### วิธีการติดตั้ง
1. **ข้อกำหนดเบื้องต้น**: Python >= 3.10 และเครื่องมือ uv (สำหรับจัดการ virtual environment และ dependencies)
2. **ขั้นตอนติดตั้ง**:
   - เปิด Terminal (PowerShell) ในโฟลเดอร์โปรเจกต์ (d:\OOP-2-2568)
   - สร้างโปรเจกต์และ virtual environment: 
     ```
     uv init
     uv venv
     ```
   - ติดตั้งไลบรารีที่จำเป็น (Pygame):
     ```
     uv add pygame
     ```
   - ตรวจสอบว่าไฟล์ pyproject.toml มี dependencies ดังนี้:
     ```
     dependencies = [
         "pygame>=2.6.1",
     ]
     ```

#### วิธีการรันเกม
- หลังติดตั้งเสร็จ ให้รันคำสั่งใน Terminal:
  ```
  uv run main.py
  ```
- เกมจะเปิดหน้าต่าง Pygame ขนาด 800x600 พิกเซล ที่อัตราเฟรม 60 FPS

#### โครงสร้างและการประยุกต์ใช้ OOP และ SOLID
เกมนี้ถูก refactor เพื่อแสดงการประยุกต์ใช้หลักการ OOP (Object-Oriented Programming) และ SOLID Principles อย่างชัด ดังนี้:

##### OOP Principles
1. **Inheritance (การสืบทอด)**:
   - **GameObject Hierarchy**: คลาสฐานสำหรับวัตถุเกมทั้งหมด (Bullet, Player, Enemy, Meteor, Pill) สืบทอดจาก GameObject ซึ่งมีฟังก์ชันพื้นฐานเช่น update(), draw(), และ collision detection
   - **Enemy Hierarchy**: Enemy เป็น abstract base class สำหรับ EnemyShip, UFOEnemy, และ BigUFOBoss เพื่อแชร์พฤติกรรมทั่วไป

2. **Polymorphism (รูปแบบหลากหลาย)**:
   - **Strategy Pattern**: ใช้สำหรับ BulletBehavior (LinearBulletBehavior สำหรับยิงตรง, HomingBulletBehavior สำหรับตามเป้าหมาย) และ EnemyBehavior (StandardEnemyBehavior, UFOBehavior) ทำให้สามารถเปลี่ยนพฤติกรรมได้แบบ runtime โดยไม่แก้ไขคลาสหลัก

3. **Encapsulation (การห่อหุ้ม)**:
   - คุณสมบัติส่วนตัว (private attributes) เช่น _health, _speed ใน Player ใช้ @property และ @setter เพื่อควบคุมการเข้าถึงและ validation (เช่น เลือดไม่ต่ำกว่า 0)
   - Composition over Inheritance: Player ประกอบด้วย StarSystem และ ShieldSystem แทนที่จะสืบทอด เพื่อความยืดหยุ่นและหลีกเลี่ยงปัญหา fragile base class

##### SOLID Principles
1. **Single Responsibility**: แต่ละคลาสมีหน้าที่เดียว เช่น Player จัดการสถานะผู้เล่น, CollisionDetector จัดการการชน, Renderer จัดการการวาดภาพ
2. **Open/Closed**: คลาสเปิดรับการขยาย (เช่น เพิ่ม Enemy ใหม่) แต่ปิดการแก้ไขโค้ดเดิม
3. **Liskov Substitution**: Enemy ย่อยสามารถแทนที่ Enemy ได้โดยไม่เปลี่ยนพฤติกรรม
4. **Interface Segregation**: ใช้ interfaces เช่น Drawable และ Collidable แยกความรับผิดชอบ
5. **Dependency Inversion**: ใช้ Factory Pattern (EnemyFactory, PowerUpFactory) และ Dependency Injection (เช่น ฉีด Player เข้า Enemy) เพื่อลด coupling

โครงสร้างโค้ดแบ่งเป็นโมดูลชัดเจน (core/, entities/, projectiles/) และใช้ Facade Pattern ใน GameEngine เพื่อจัดการระบบย่อยทั้งหมด (SpawningManager, AudioManager, Renderer) ทำให้โค้ดอ่านง่าย ทดสอบได้ และขยายได้สะดวก

หากต้องการข้อมูลเพิ่มเติมหรือแก้ไขโค้ด สามารถสอบถามได้!- เกมจะเปิดหน้าต่าง Pygame ขนาด 800x600 พิกเซล ที่อัตราเฟรม 60 FPS

#### โครงสร้างและการประยุกต์ใช้ OOP และ SOLID
เกมนี้ถูก refactor เพื่อแสดงการประยุกต์ใช้หลักการ OOP (Object-Oriented Programming) และ SOLID Principles อย่างชัด ดังนี้:

##### OOP Principles
1. **Inheritance (การสืบทอด)**:
   - **GameObject Hierarchy**: คลาสฐานสำหรับวัตถุเกมทั้งหมด (Bullet, Player, Enemy, Meteor, Pill) สืบทอดจาก GameObject ซึ่งมีฟังก์ชันพื้นฐานเช่น update(), draw(), และ collision detection
   - **Enemy Hierarchy**: Enemy เป็น abstract base class สำหรับ EnemyShip, UFOEnemy, และ BigUFOBoss เพื่อแชร์พฤติกรรมทั่วไป

2. **Polymorphism (รูปแบบหลากหลาย)**:
   - **Strategy Pattern**: ใช้สำหรับ BulletBehavior (LinearBulletBehavior สำหรับยิงตรง, HomingBulletBehavior สำหรับตามเป้าหมาย) และ EnemyBehavior (StandardEnemyBehavior, UFOBehavior) ทำให้สามารถเปลี่ยนพฤติกรรมได้แบบ runtime โดยไม่แก้ไขคลาสหลัก

3. **Encapsulation (การห่อหุ้ม)**:
   - คุณสมบัติส่วนตัว (private attributes) เช่น _health, _speed ใน Player ใช้ @property และ @setter เพื่อควบคุมการเข้าถึงและ validation (เช่น เลือดไม่ต่ำกว่า 0)
   - Composition over Inheritance: Player ประกอบด้วย StarSystem และ ShieldSystem แทนที่จะสืบทอด เพื่อความยืดหยุ่นและหลีกเลี่ยงปัญหา fragile base class

##### SOLID Principles
1. **Single Responsibility**: แต่ละคลาสมีหน้าที่เดียว เช่น Player จัดการสถานะผู้เล่น, CollisionDetector จัดการการชน, Renderer จัดการการวาดภาพ
2. **Open/Closed**: คลาสเปิดรับการขยาย (เช่น เพิ่ม Enemy ใหม่) แต่ปิดการแก้ไขโค้ดเดิม
3. **Liskov Substitution**: Enemy ย่อยสามารถแทนที่ Enemy ได้โดยไม่เปลี่ยนพฤติกรรม
4. **Interface Segregation**: ใช้ interfaces เช่น Drawable และ Collidable แยกความรับผิดชอบ
5. **Dependency Inversion**: ใช้ Factory Pattern (EnemyFactory, PowerUpFactory) และ Dependency Injection (เช่น ฉีด Player เข้า Enemy) เพื่อลด coupling

โครงสร้างโค้ดแบ่งเป็นโมดูลชัดเจน (core/, entities/, projectiles/) และใช้ Facade Pattern ใน GameEngine เพื่อจัดการระบบย่อยทั้งหมด (SpawningManager, AudioManager, Renderer) ทำให้โค้ดอ่านง่าย ทดสอบได้ และขยายได้สะดวก