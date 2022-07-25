from django.test import TestCase, Client # Client : 웹사이트를 방문하는 사람의 브라우저
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        # 1-1. NavBar가 있다.
        navbar = soup.nav

        # 1-2. 로고를 클릭하면 메인 페이지에 접속한다.
        logo_btn = navbar.find('a', text='Do It Django') # content가 'Do It Django'인 a태그 찾기
        self.assertEqual(logo_btn.attrs['href'], '/') # attrs['속성이름'] : attribute 값

        # 1-3. 'Home'을 클릭하면 메인 페이지에 접속한다.
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(logo_btn.attrs['href'], '/')

        # 1-4. 'Blog'를 클릭하면 포스트 리스트 페이지에 접속한다.
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        # 1-5. 'About me'를 클릭하면 About me 페이지에 접속한다.
        about_me_btn = navbar.find('a', text='About me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    # 'test_'로 시작하는 함수는 unit test로 인식됨
    # 현재 데이터베이스와 전혀 상관없는 테스트용 새로운 데이터베이스가 만들어짐
    def test_post_list(self):
        # 1-1. 포스트 목록 페이지(post_list)를 연다.
        response = self.client.get('/blog/')

        # 1-2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200) # assertEqual(a,b) => a와 b가 같다.

        # 1-3. 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser') # response의 내용물이 html임을 알려줌
        self.assertIn('Blog', soup.title.text) # assertIn(a,b) => b안에 a가 있다.

        # 1-4. navbar 테스트
        self.navbar_test(soup)

        # 2-1. 게시물이 하나도 없을 때,
        self.assertEqual(Post.objects.count(), 0)

        # 2-2. 메인 영역에 "아직 게시물이 없습니다." 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area') # id가 'main-area'인 div태그 찾기
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

    # 'test_'로 시작하는 함수는 unit test로 인식됨
    # 현재 데이터베이스와 전혀 상관없는 테스트용 새로운 데이터베이스가 만들어짐
    def test_post_detail(self):
        # 1-1. 포스트가 하나 있다.
        post_001 = Post.objects.create(
            # Post 모델에 기반한 테스트 게시물 작성
            title='첫번째 포스트 제목',
            content='첫번째 포스트 내용',
        )
        self.assertEqual(Post.objects.count(), 1)

        # 1-2. 그 포스트의 url은 '/blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫번째 포스트의 상세페이지 테스트
        # 2-1. 첫번째 포스트의 url로 접근하면 정상적으로 response가 온다. (status code : 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 2-2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)

        # 2-3. 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2-4. 첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2-5. 첫번째 포스트의 작성자(author)가 포스트 영역에 있다. (아직 구현할 수 없음)

        # 2-6. 첫번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)