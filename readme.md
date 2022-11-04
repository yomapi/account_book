# 1. Config, Install in Local & Docker

### config

configs/config 경로에 config_real.yml 파일을 만들어 설정 값을 넣어주세요.

```yaml
# configs/config_example.yml
# use this example for config_real.yml

databases:
  host: "host url"
  port: 3306
  database: "db name"
  username: "username"
  password: "passwd"
  timezone: "+09:00"

secrets:
  django: "django-something-something"

token:
  scret: "something_secret"
  expire_sec: 3600
```

### Install in local

```bash
poetry install
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### build docker image and run

```bash
docker build -t your_image_name .
docker run -p 8000:8000 your_image_name
```

# 2. Database

![스크린샷 2022-11-04 오후 5.12.14.png](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/82bd7835-149c-4915-9fc6-2c41ce678f95/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2022-11-04_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_5.12.14.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221104%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221104T084752Z&X-Amz-Expires=86400&X-Amz-Signature=3d1465de82f2192652a837245a9e19d11f8fe1e8ae195ded9261adc73776a909&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA%25202022-11-04%2520%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE%25205.12.14.png%22&x-id=GetObject)

- 로그아웃을 위해서 jwt을 저장할, token 테이블 사용
- 모든 테이블은 deleted_at을 이용하여 soft delete로 구현

# 3. API Documentaion

## User

### 1. signup

- url: signup/
- method: POST
- body
    
    
    | key      | datatype |
    | -------- | -------- |
    | email    | str      |
    | password | str      |
- response
    
    ```json
    {
        "id": 10,
        "created_at": "2022-11-04T08:17:33.728675Z",
        "updated_at": "2022-11-04T08:17:33.728900Z",
        "deleted_at": null,
        "email": "test12@test.com",
        "password": "$2b$12$iAbDrzR/LP30CBY2HaCxxeWasQa526PfTFImICGftWDyTuJ1ZwA36"
    }
    ```
    

### 2. login

- url: login/
- method: POST
- body
    
    
    | key      | datatype |
    | -------- | -------- |
    | email    | str      |
    | password | str      |
- response
    
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NiwiZXhwIjoxNjY3NTUzNTE0Ljc5NDgyMX0.TeLjkuawFEcljTN3UtWKPfz4fHTHHDH6niqB2W8sNYw"
    }
    ```
    

### 3. logout

- url: logout/
- method: POST
- header
    
    
    | Authorization | 로그인 시 받은, access 키 |
    | ------------- | ------------------------- |
- response
    
    ```json
    {"success": true}
    ```
    

## Book(가계부)

- 모든 request는 header에 access 토큰을 넣어줍니다

### 1.생성

- url: /book/
- method: POST
- request
    
    ```json
    {
        "memo": "콜라",
        "amount": 1200
    }
    
    ```
    
- response
    
    ```json
    {
        "id": 48,
        "amount": 1200,
        "memo": "콜라",
        "user": 6
        "created_at": "2022-11-04T08:35:00.281719Z",
        "updated_at": "2022-11-04T08:35:00.281788Z",
        "deleted_at": null,
    }
    ```
    

1. 수정
- url: book/<book_id>
- method: POST
- request
    
    ```json
    {
        "memo": "제로 콜라",
        "amount": 1300
    }
    ```
    

- response
    
    ```json
    {
        "id": 48,
        "created_at": "2022-11-04T08:35:00.281719Z",
        "updated_at": "2022-11-04T08:36:11.487139Z",
        "deleted_at": null,
        "amount": 1300,
        "memo": "제로 콜라",
        "user": 6
    }
    ```
    

1. 삭제
- url: [book/](http://127.0.0.1:8000/book/1/)<book_id>/
- method: DELETE
- response
    
    ```json
    {"success": true}
    ```
    

1. 복구
- url: [book/](http://127.0.0.1:8000/book/1/)<book_id>/recovery/
- method: POST
- response

```json
{
    "id": 48,
    "created_at": "2022-11-04T08:35:00.281719Z",
    "updated_at": "2022-11-04T08:38:41.561777Z",
    "deleted_at": null,
    "amount": 1300,
    "memo": "제로콜라",
    "user": 6
}
```

1. 상세 조회
- url: [book/](http://127.0.0.1:8000/book/1/)<book_id>/
- method: GET
- response
    
    ```json
    {
        "id": 48,
        "created_at": "2022-11-04T08:35:00.281719Z",
        "updated_at": "2022-11-04T08:38:41.561777Z",
        "deleted_at": null,
        "amount": 1300,
        "memo": "제로콜라",
        "user": 6
    }
    ```
    

1. 목록 조회
- url: [book/](http://127.0.0.1:8000/book/1/)
- method: GET
- response
    
    ```json
    {
        "count": 3,
        "data": [
            {
                "id": 48,
                "created_at": "2022-11-04T08:35:00.281719Z",
                "updated_at": "2022-11-04T08:38:41.561777Z",
                "deleted_at": null,
                "amount": 1300,
    				    "memo": "제로콜라",
                "user": 6
            },
            {
                "id": 49,
                "created_at": "2022-11-04T08:39:50.818838Z",
                "updated_at": "2022-11-04T08:39:50.818889Z",
                "deleted_at": null,
                "amount": 123,
    				    "memo": "제로콜라",
                "user": 6
            },
            {
                "id": 50,
                "created_at": "2022-11-04T08:39:51.629760Z",
                "updated_at": "2022-11-04T08:39:51.629809Z",
                "deleted_at": null,
                "amount": 123,
    				    "memo": "제로콜라",
                "user": 6
            }
        ]
    }
    ```