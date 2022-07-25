from django.test import TestCase, Client # Client : 웹사이트를 방문하는 사람의 브라우저
from bs4 import BeautifulSoup
from .models import Post


# 현재 데이터베이스와 전혀 상관없는 테스트용 새로운 데이터베이스가 만들어짐
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1-1. 포스트 목록 페이지(post_list)를 연다.
        response = self.client.get('/blog/')

        # 1-2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200) # assertEqual(a,b) => a와 b가 같다.

        # 1-3. 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser') # response의 내용물이 html임을 알려줌
        self.assertIn('Blog', soup.title.text)

        # 1-4. NavBar가 있다.
        navbar = soup.nav

        # 1-5. Blog, About me 라는 문구가 NavBar에 있다.
        self.assertIn('Blog', navbar.text) # assertIn(a,b) => b안에 a가 있다.
        self.assertIn('About me', navbar.text)

        # 2-1. 게시물이 하나도 없을 때,
        self.assertEqual(Post.objects.count(), 0)

        # 2-2. 메인 영역에 "아직 게시물이 없습니다." 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3-1. 만약 게시물이 2개 있다면,
        post_001 = Post.objects.create(
            # Post 모델에 기반한 테스트 게시물 작성
            title='첫번째 포스트 제목',
            content='첫번째 포스트 내용',
        )
        post_002 = Post.objects.create(
            # Post 모델에 기반한 테스트 게시물 작성
            title='두번째 포스트 제목',
            content='두번째 포스트 내용',
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3-2. 포스트 목록 페이지를 새로 고침 했을 때,
        response = self.client.get('/blog/')

        # 3-3. 메인 영역에 포스트 2개의 타이틀이 존재한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3-4. "아직 게시물이 없습니다." 라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text) # assertNotIn(a,b) => b안에 a가 없다.