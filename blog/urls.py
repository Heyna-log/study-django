from django.urls import path
from . import views

urlpatterns = [
    # <int:pk> -> :뒤에 있는 pk : view에 전달되는 파라미터명 / :앞에 있는 int : Path Converter(view에 값을 전달하기 전에 콜론 앞의 타입으로 변환 후 파라미터로 전달)
    # Path Converter 종류
        # str : 문자열 리턴. 단, 빈 문자열은 포함 안함, 경로를 표시하는 / 문자는 포함 안함. 만약 별도의 path converter를 지정하지 않으면 이 str을 디폴트로 사용
        # int : 0 이상의 정수. Integer 리턴.
        # slug : 영문 대소문자와 숫자, 그리고 하이폰(-)과 밑줄(_)을 갖는 문자열 리턴.
        # uuid : UUID를 가리키며, 모든 문자가 소문자이어야 하고 대시(-)가 포함되어야 함. 이 converter는 uuid.UUID 객체를 리턴함.
        # path : 경로에 사용되는 슬래쉬(/)를 포함하는 문자열 리턴.
    path('<int:pk>/', views.single_post_page), # 'blog/pk(int형)/' url일때 blog.views.single_post_page 함수 호출
    # path('', views.index), # blog.views.index 함수 호출
    path('', views.PostList.as_view()) # CBV
]
