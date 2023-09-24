from fastapi import FastAPI, Path
# Pydanticは、データのバリデーションを行うためのライブラリ
# Pythonの型ヒントを使ってデータモデルを定義し、これをもとにデータのバリデーションを行う
from pydantic import BaseModel
# Optionalは、Pythonのtypingモジュールに含まれる型ヒントの一つ
# 特定の型もしくはNoneの値をとることができる
# 主に関数のパラメーターがOptionalで,与えられていない場合に'None'としてデフォルト値を設定するために使われる
# これは特にAPIエンドポイントのパラメーターがオプショナルである場合に便利
from typing import Optional

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    course: str


# Optionalを使用することで、フロントエンドが送信するデータの一部のみを更新することができる
# 例えば、フロントエンドが年齢のみを更新する場合、nameとyearはNoneとして送信される
# また、Optionalを使用することで、どのフィールドが必須であるかを明示的に示すことができ、
# APIのドキュメンテーションと型検査の両方に役立つ
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None


students = {
    1: {
        "name": "john",
        "age": 17,
        "course": "advance"},
    2: {
        "name": "carl",
        "age": 16,
        "course": "basic"}
}


@app.get("/")
async def root():
    return {"message": "What your name ?"}


@app.get("/students/")
def get_students():
    return students


# {student_id}は、パスパラメーターでリクエストURLの一部として送信される
@app.get("/students/{student_id}")
# Pathは、fastapiのパスパラメーターのバリデーションを行うためのクラスで、
# `...`は、パスパラメーターが必須であることを示す
# descriptionは、パスパラメーターの説明を記述する
# gt(greater than)とlt(less than)は、パスパラメーターの値の範囲を指定する
# この場合、student_idは1より大きく、3より小さい値である必要がある
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=3)):
    return students[student_id]


# パスパラメーターの代わりに、クエリパラメーターを使用することもできる
# クエリパラメーターは、リクエストURLの後に?を付けて送信される
# クエリパラメーターは、パスパラメーターとは異なり、必須ではない
# `get_student`関数は`name`というオプショナルなクエリパラメーターを受け取る
# fastapiは、特定のパラメータがパスパラメータやリクエストボディでないとき、クエリパラメータであると推定する
# 型ヒントを使用することで、fastapiはクエリパラメーターの値を適切な型に変換する
# URLは、`/get_by_name?name=john`のようになる
@app.get("/get_by_name")
def get_student(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}


@app.post("/students/{student_id}")
# `student`は変数で、`Student`はPydanticモデル
# Pydanticモデルは、リクエストボディのバリデーションとデータの変換を行う
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student.model_dump()
    return students[student_id]


@app.put("/students/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    update_data = student.model_dump(exclude_unset=True)
    students[student_id].update(update_data)

    # if student.name is not None:
    #     students[student_id].name = student.name
    #
    # if student.age is not None:
    #     students[student_id].age = student.age
    #
    # if student.year is not None:
    #     students[student_id].course = student.course

    return students[student_id]


@app.delete("/delete_student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    # delは参照の作をを行う
    # その後、非同期でガベージコレクションが実行され、物理的な削除（メモリの解放）が行われる
    del students[student_id]
    return {"Message": "Student deleted successfully"}
