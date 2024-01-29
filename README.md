Code dùng để crawl dữ liệu báo cáo tài chính từ website cafef.vn. Xây dựng hệ thống phân tích dữ liệu chứng khoán tự động bằng công cụ Transform dbt (Data Build Tool), kho dữ liệu BigQuery và BI Locker Studio.

**Kiến trúc hệ thống**
![image](https://github.com/rossery0204/scrappeBCTC/assets/104888871/c2a17d79-9db1-481f-989e-6a9c215e0192)

**Chức năng các file**
run_by_trigger.py: crawl dữ liệu manually
run_by_schedule.py: crawl dữ liệu giá hàng ngày

**Cài đặt và kết nối dbt và BigQuery**
Sử dụng code transform trên dbt https://github.com/rossery0204/dbtDA2 

**Data Model OLAP** (chấp nhận dư thừa dữ liệu)
![image](https://github.com/rossery0204/scrappeBCTC/assets/104888871/4b5bae4d-f5a9-49aa-8789-401ccd99e2ab)

**Trực quan hóa trên Locker Studio**
![image](https://github.com/rossery0204/scrappeBCTC/assets/104888871/68725312-b60c-4510-baea-8f9996735f0c)
![Uploading image.png…]()

