from django.db import models
from django.contrib.auth.models import User
import os

class Post(models.Model):
    # 제목
    # CharField : 텍스트가 짧을 때
    # max_length : 글자 최대 길이
    title = models.CharField(max_length=50)

    # 내용
    # TextField : 텍스트가 길 때
    content = models.TextField()

    # 이미지
    # blank=True : null 허용
    # upload_to='blog/images/%y/%m/%d/' : blog/images/년/월/일 경로에 파일 저장
    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)

    # 파일 업로드
    file_upload = models.FileField(upload_to='blog/images/%y/%m/%d/', blank=True)

    # 작성일
    # auto_now_add=True : 새로 생성될 때 현재시간을 자동으로 입력
    created_at = models.DateTimeField(auto_now_add=True)

    # 수정일
    # auto_now=True : 이미 생성되어 있고 업데이트하는 경우 수정할 때의 현재 시간을 자동으로 입력
    updated_at = models.DateTimeField(auto_now=True)

    # 작성자
    # 다대일 관계
    # on_delete=models.CASCADE : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제됨.
    # on_delete=models.SET_NULL : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 null로 바꾼다. (null=True일 때만 가능)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self): # __str__ : 출력 시 문자열로 나옴
        return f'[{self.pk}] {self.title} - {self.author}' # f'{}' -> 포메팅

    def get_absolute_url(self): # 각 포스트 고유의 url 생성 (장고에서 기본 제공하는 기능)
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) # 파일 이름

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # 파일 이름에서 확장자('.'으로 자른 배열의 마지막 인덱스) 가져오기