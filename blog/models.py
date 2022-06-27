from django.db import models

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

    # author : 추후 작성 예정

    def __str__(self): # __str__ : 출력 시 문자열로 나옴
        return f'[{self.pk}] {self.title}' # f'{}' -> 포메팅인가..?

    def get_absolute_url(self): # 각 포스트 고유의 url 생성 (장고에서 기본 제공하는 기능)
        return f'/blog/{self.pk}/'