from django.db import models
from django.contrib.auth.models import User
import os


class Category(models.Model):
    # 카테고리 이름
    # unique=True : 중복 비허용
    name = models.CharField(max_length=50, unique=True)

    # 슬러그 : 이미 확보된 데이터를 사용하여 읽기 쉬운 형식의 url 생성. url이므로 중복되면 안됨!(unique=True)
    # allow_unicode=True : 한글 사용 가능(특수기호 제외)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta: # 권한, 데이터베이스 이름, 단 복수 이름, 추상화, 순서 지정 등과 같은 모델에 대한 다양한 사항을 정의하는 데 사용
        # verbose_name_plural : 모델에 대해 사람이 읽을 수 있는 복수형 이름을 정의하는 데 사용. Django의 기본 명명 규칙을 덮어씀. 이 이름은 관리자 패널 (/admin/)에도 반영됨.
        verbose_name_plural = 'Categories'
        # 다른 meta 옵션 참고 : https://www.delftstack.com/ko/howto/django/class-meta-in-django/


class Post(models.Model):
    # 제목
    # CharField : 텍스트가 짧을 때
    # max_length : 글자 최대 길이
    title = models.CharField(max_length=50)

    # 내용
    # TextField : 텍스트가 길 때
    content = models.TextField()

    # 이미지
    # blank=True : 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용. 장고 관리자(admin) 및 직접 정의한 폼에도 반영됨.
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
    # null=True : 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용
    # on_delete=models.CASCADE : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제됨.
    # on_delete=models.SET_NULL : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 null로 바꾼다. (null=True일 때만 가능)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 카테고리
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self): # __str__ : 출력 시 문자열로 나옴
        return f'[{self.pk}] {self.title} - {self.author}' # f'{}' -> 포메팅

    def get_absolute_url(self): # 각 포스트 고유의 url 생성 (장고에서 기본 제공하는 기능)
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) # 파일 이름

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # 파일 이름에서 확장자('.'으로 자른 배열의 마지막 인덱스) 가져오기