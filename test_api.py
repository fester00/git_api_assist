import os
import unittest
from dotenv import load_dotenv
import requests
from requests import exceptions

load_dotenv(override=True)

DATAS={
        'GITHUB_USERNAME' : os.getenv('GITHUB_USERNAME'),
        'GITHUB_TOKEN' : os.getenv('GITHUB_TOKEN'),
        'REPOSITORY_NAME' : os.getenv('REPOSITORY_NAME'),
        }

class Git_tasks():
    DATAS = DATAS

    def __init__(self, url: str) -> None:
        if not url:
            raise ValueError("URL должен быть не пустым")
        self.url = url
        pass

    # Get all repositories #

    def get_repos(self):
        response = requests.get(url=self.url,
                                 headers={
                                     'Authorization': f'Bearer {self.DATAS["GITHUB_TOKEN"]}'
                                 })

        if response.status_code == 200:
            print(f"Список репозиториев: {[f'{i+1} {el["name"]}' for i, el in enumerate(response.json())]}")
        else:
            raise requests.exceptions.HTTPError(f'Failed to GET repositories. Status code:{response.status_code}')
        return response
    # Add new repos #

    def add_repos(self, repo_name, repo_description, private=True):
        response = requests.post(
            url=self.url,
            headers={
                'Authorization': f'Bearer {self.DATAS["GITHUB_TOKEN"]}',
                'Content-Type': 'application/json'
            },
            json={
                'name': repo_name,
                'description': repo_description,
                'private': private
            }
        )

        if response.status_code == 201:
            print(f'Repo is Created Succes =)')
        elif response.status_code == 422:
            raise requests.exceptions.HTTPError(f'Failed to create repository. Status code:{response.status_code}')
        else:
            raise requests.exceptions.HTTPError(f'Failed to POST request. Status code: {response.status_code}')
        return response
    # Del repos #

    def del_repos(self,repo_name):
        response = requests.delete(f'https://api.github.com/repos/{self.DATAS['GITHUB_USERNAME']}/{repo_name}',
                                  
                                    headers={
                                        'Authorization': f'Bearer {self.DATAS["GITHUB_TOKEN"]}',
                                        "Accept": "application/vnd.github.v3+json",
                                    })
                                     

        if response.status_code == 204:
            print("Репозиторий удален!")
        elif response.status_code == 401:
            raise requests.exceptions.HTTPError(f'Failed to DELETE request. Status code: {response.status_code}')
        else:
            raise requests.exceptions.HTTPError(f'Failed to delete repository. Status code:{response.status_code}')
        return response
    # Chek needed params pre work status #

    def chek_conf(self):
        for k, v in self.DATAS.items():
            if not v:
                print(f'\nNot found {k}\n')
            else:
                print( f'\n{k} IS - - -  OK')

        if all(self.DATAS.values()):
            print("\nAll necessary parameters are available.\n")
            return
        else:
            raise ValueError("Some necessary parameters are missing.")



class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        self.git = Git_tasks('https://api.github.com/user/repos')  # Создаем экземпляр нашего класса

    def test_get_repos(self):
        response = self.git.get_repos()
        self.assertEqual(response.status_code, 200 or 201 or 204)  # Проверяем статус-код ответа

    def test_add_repo(self):
        repo_name = 'test-repo'
        repo_description = 'Тестовый репозиторий'
        self.git.add_repos(repo_name, repo_description)
        response = self.git.get_repos()
        self.assertIn(repo_name, [el['name'] for el in response.json()])  # Проверяем, создан ли репозиторий

    def test_del_repo(self):
        repo_name = 'test-repo'
        response = self.git.del_repos(repo_name)
        self.assertEqual(response.status_code,  204)  # Проверяем статус-код ответа

if __name__ == '__main__':
    unittest.main()