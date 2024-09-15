
# Создайте файл .env в корне проекта и добавьте ваши данные

GITHUB_TOKEN=token
GITHUB_USERNAME=name
REPOSITORY_NAME=repo_name



git = Git_tasks(url='https://api.github.com/user/repos')

# Получить список репозиториев
git.get_repos()

# Создать новый репозиторий
git.add_repos('Новый репозиторий', 'Описание репозитория')

# Удалить репозиторий
git.del_repos('Новый репозиторий')


## Chek needed params pre work status

Чтобы проверить, доступны ли все необходимые параметры перед выполнением операций, вы можете вызвать метод
git.chek_conf()# git_api_assist
