from django.contrib.auth.models import User
from django.test import TestCase, Client
from game.models import Game, Team


class TestResultsPage(TestCase):
    def test_page_availability(self):
        client = Client()
        response = client.get('/results/')
        self.assertEquals(200, response.status_code)

    def test_page_without_results(self):
        client = Client()
        response = client.get('/results/')
        self.assertContains(response, '<div class="scores"')
        self.assertContains(response, 'No scores registered yet')
        self.assertNotContains(response, '<ul class="score-board"')
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, 'No result yet')

    def test_page_with_results(self):
        # create 2 users (automatically creates corresponding teams)
        laurent = User.objects.create_user('laurent', 'laurent@test.com', 'pass')
        laurent.save()
        laurent_team = laurent.teams.all()[0]

        rolf = User.objects.create_user('rolf', 'rolf@test.com', 'pass')
        rolf.save()
        rolf_team = rolf.teams.all()[0]

        # create 1 game
        game = Game.objects.create(winner=laurent_team, loser=rolf_team)
        game.save()

        client = Client()
        response = client.get('/results/')

        self.assertContains(response, '<div class="scores"')
        self.assertNotContains(response, 'No scores registered yet')
        self.assertContains(response, '<ol class="score-board"')
        self.assertContains(response, '<li class="score-item"', 2)
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, '<ul class="games')
        self.assertContains(response, '<li class="game-item', 1)

        # specifically test ranking
        self.assertContains(response, '<li class="score-item">laurent (1028)</li>')
        self.assertContains(response, '<li class="score-item">rolf (971)</li>')

        # create a 2nd game (as usual Laurent wins)
        game = Game.objects.create(winner=laurent_team, loser=rolf_team)
        game.save()

        response = client.get('/results/')
        self.assertContains(response, '<li class="score-item">laurent (1037)</li>')
        self.assertContains(response, '<li class="score-item">rolf (962)</li>')