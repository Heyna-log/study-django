from django.test import TestCase, Client # Client : 웹사이트를 방문하는 사람의 브라우저
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category


class TestView(TestCase):
    # unit test 시작 전 실행되는 기본 세팅용 함수
    def setUp(self):
        # 클라이언트
        self.client = Client()

        # 테스트용 user 생성
        self.user_test1 = User.objects.create_user(
            username='test1',
            password='1111'
        )
        self.user_test2 = User.objects.create_user(
            username='test2',
            password='1111'
        )

        # 테스트용 카테고리 생성 (Category 모델 기반)
        self.category_programming = Category.objects.create(
            name='programming',
            slug='programming'
        )
        self.category_music = Category.objects.create(
            name='music',
            slug='music'
        )

        # Post 모델에 기반한 테스트 게시물 작성
        self.post_001 = Post.objects.create(
            title='첫번째 포스트 제목',
            content='첫번째 포스트 내용',
            author=self.user_test1,
            category=self.category_programming,
        )
        self.post_002 = Post.objects.create(
            title='두번째 포스트 제목',
            content='두번째 포스트 내용',
            author=self.user_test2,
            category=self.category_music,
        )
        self.post_003 = Post.objects.create(
            title='세번째 포스트 제목',
            content='세번째 포스트 내용',
            author=self.user_test2,
        )

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

    def categories_card_test(self, soup):
        # 1-1. 카테고리 카드 영역에 'Categories'가 있다.
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)

        # 2-1. 게시물이 1개 이상 있을 때,
        # self.assertGreaterEqual(Post.objects.count(), 1)

        # 2-2. 카테고리 카드 영역에 '카테고리 이름 (해당 카테고리 게시물 개수)'가 있다.
        # 등록된 카테고리 일 때
        for i in Category.objects.all():
            self.assertIn(f'{i} ({i.post_set.count()})', categories_card.text)
        # 등록 안 된 카테고리 일 때
        self.assertIn(f'미분류 ({Post.objects.filter(category=None).count()})', categories_card.text)

    # 'test_' 시작하는 함수는 unit test로 인식됨
    # 현재 데이터베이스와 전혀 상관없는 테스트용 새로운 데이터베이스가 만들어짐[setUp(self) 기반]
    def test_post_list_with_posts(self):
        # 1. 게시물이 존재한다.
        self.assertGreater(Post.objects.count(), 0)  # assertGreater(a,b) => a가 b보다 크다. [a > b]

        # 2-1. 포스트 목록 페이지(post_list)를 연다.
        response = self.client.get('/blog/')

        # 2-2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200) # assertEqual(a,b) => a와 b가 같다.

        # 3-1. navbar, categories_card 테스트
        soup = BeautifulSoup(response.content, 'html.parser')  # response의 내용물이 html임을 알려줌
        self.navbar_test(soup)
        self.categories_card_test(soup)

        # 3-2. 페이지의 타이틀에 Blog라는 문구가 있다.
        self.assertIn('Blog', soup.title.text) # assertIn(a,b) => b안에 a가 있다.

        # 3-3. 메인 영역에 "아직 게시물이 없습니다." 라는 문구가 없어야 한다.
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)  # assertNotIn(a,b) => b안에 a가 없다.

        # 3-4. 각각의 포스트 카드 영역에 게시물의 타이틀, 작성자(대문자), 카테고리 이름이 존재한다.
        num = 0 # 변수 선언을 위한 카운트
        for i in Post.objects.all():
            num = num + 1
            globals()['post_card_{}_area'.format(num)] = main_area.find('div', id='post_card_{}'.format(num)) # 동적 변수 생성
            card_area = globals()['post_card_{}_area'.format(num)]
            # 타이틀 유무 확인
            self.assertIn(i.title, card_area.text)
            # 작성자(대문자) 유무 확인
            self.assertIn(i.author.username.upper(), card_area.text) # upper() : 대문자로 출력
            # 카테고리 이름 유무 확인
            if i.category in Category.objects.all():  # Category 안에 i.category가 있으면 True
                self.assertIn(i.category.name, card_area.text)  # 카테고리 이름 유무 확인
            elif i.category is None:  # 카테고리가 등록 안 된 게시물일 경우(category는 null=True, blank=True 이므로)
                self.assertIn('미분류', card_area.text)

        print('test_post_list_with_posts 완료')

    def test_post_list_without_post(self):
        # 게시물이 하나도 없는 상태 만들기
        Post.objects.all().delete()

        # 1-1. 게시물이 하나도 없다.
        self.assertEqual(Post.objects.count(), 0)

        # 2-1. 포스트 목록 페이지(post_list)를 연다.
        response = self.client.get('/blog/')

        # 2-2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 3-1. navbar, categories_card 테스트
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.categories_card_test(soup)

        # 3-2. 페이지의 타이틀에 Blog라는 문구가 있다.
        self.assertIn('Blog', soup.title.text)

        # 3-3. 메인 영역에 "아직 게시물이 없습니다." 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area') # id가 'main-area'인 div태그 찾기
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        print('test_post_list_without_post 완료')

    # 'test_'로 시작하는 함수는 unit test로 인식됨
    # 현재 데이터베이스와 전혀 상관없는 테스트용 새로운 데이터베이스가 만들어짐[setUp(self) 기반]
    def test_post_detail(self):
        # 1-1. 게시물이 1개 이상 있다.
        self.assertGreaterEqual(Post.objects.count(), 1) # assertGreaterEqual(a,b) : a가 b와 같거나 b보다 크다. [a >= b]

        # 1-2. 첫번째 게시물의 url은 '/blog/1/' 이다.
        post = Post.objects.first()
        self.assertEqual(post.get_absolute_url(), '/blog/1/')

        # 2. 첫번째 게시물의 상세페이지 테스트
        # 2-1. 첫번째 게시물의 url로 접근하면 정상적으로 response가 온다. (status code : 200)
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 2-2. 게시물 목록 페이지와 똑같은 내비게이션 바가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)

        # 2-3. 첫번째 게시물의 제목이 웹 브라우저 탭 타이틀에 들어있다.
        self.assertIn(post.title, soup.title.text)

        # 2-4. 첫번째 게시물의 제목이 게시물 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post.title, post_area.text)

        # 2-5. 첫번째 게시물의 작성자(author, 대문자)가 게시물 영역에 있다.
        self.assertIn(post.author.username.upper(), post_area.text)

        # 2-6. 첫번째 게시물의 내용(content)이 게시물 영역에 있다.
        self.assertIn(post.content, post_area.text)

        print('post_detail 완료')