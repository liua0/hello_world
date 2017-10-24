import json

import requests


class Github(object):

    def __init__(self, token):
        self.token = token
        self.header = {
            'Authorization': 'Bearer ' + self.token
        }

    def _get_data(self, url, action='get'):
        '''
        请求API
        :param url:
        :param action:HTTP访问方式
        :return: API数据
        '''
        if action == 'get':
            try:
                _data = requests.get(
                    url=url, headers=self.header, timeout=30).text
                return json.loads(_data)

            except BaseException:
                print("请检查网络！！!")
                return ""
        elif action == 'put':
            try:
                _data = requests.put(
                    url=url, headers=self.header, timeout=30).text
                return json.loads(_data)

            except BaseException:
                print("请检查网络！！!")
                return ""
        elif action == 'del':
            try:
                _data = requests.delete(
                    url=url, headers=self.header, timeout=30).text
                return json.loads(_data)
            except BaseException:
                print("请检查网络！！!")
                return ""

    def get_repos(self, type):
        '''
        获得所有的仓库
        :param type: 仓库的类型
        :return: 仓库的名字
        '''
        url = "https://api.github.com/user/repos?type=" + type
        data = self._get_data(url)
        repo_name = {}
        for item in data:
            repo_name[item['name']] = item['full_name']
        return repo_name

    def get_repo_collaborator(self, repo):
        '''
        获得仓库的开发者
        :param repo: 仓库名
        :return:
        '''
        url = 'https://api.github.com/repos/' + repo + '/collaborators'
        data = self._get_data(url)
        collaborator_names = []
        for item in data:
            collaborator_names.append(item['login'])

        print("\n正在操作的仓库是：{}：\n".format(repo))
        index = 0
        for collaborator_name in collaborator_names:
            index += 1
            print(
                "#{index} {name}".format(
                    index=index,
                    name=collaborator_name))

    def add_collaborator(self, repo_full_name, mumber):
        '''
        邀请开发者
        :param repo_full_name: 仓库的全名
        :param mumber: 需要邀请的开发者名字
        :return:
        '''
        url = "https://api.github.com/repos/" + \
            repo_full_name + "/collaborators/" + mumber.lower()
        data = self._get_data(url, action='put')
        if mumber not in data:
            print('邀请失败 请检查用户名')
        else:
            print('完成邀请{}'.format(mumber))

    def del_collaborator(self, repo_full_name, mumber):
        '''
        删除仓库中的开发者
        :param repo_full_name: 仓库的名字
        :param mumber: 需要删除的开发者
        :return:
        '''
        url = "https://api.github.com/repos/" + \
            repo_full_name + "/collaborators/" + mumber.lower()
        data = self._get_data(url, action='del')
        print(data)

    def main_muen(self):
        '''
        主菜单
        :return:
        '''
        repos = self.get_repos('public')
        repo_list = []
        index = 0
        for repo_full_name in repos.keys():
            index += 1
            repo_list.append(repos[repo_full_name])
            print(
                "#{index} {repo_name}".format(
                    index=index,
                    repo_name=repos[repo_full_name]))

        action = input("\n请选择需要进行的操作,增加或删除collaborator(add/del)：\n")
        if action == 'add' or action == 'a':

            while True:
                inputed = input('\n请输入需要操作的仓库:')

                if inputed.isdigit():

                    if 0 < int(inputed) <= len(repo_list):
                        repo = repo_list[int(inputed) - 1]
                        self.get_repo_collaborator(repo)
                        mumber = input("请输入需要操作的用户：")
                        self.add_collaborator(repo, mumber)
                        break

                    else:
                        print("输入错误！！！")

                elif inputed in repos:
                    gh.get_repo_collaborator(repos[inputed])
                    break
                else:
                    print("输入错误！！！")
        elif action == 'del' or action == 'd':
            while True:
                inputed = input('\n请输入需要操作的仓库:')
                if inputed.isdigit():
                    if 0 < int(inputed) < len(repo_list) + 1:
                        repo = repo_list[int(inputed) - 1]
                        self.get_repo_collaborator(repo)
                        mumber = input("请输入需要操作的用户：")
                        self.del_collaborator(repo, mumber)
                        break

                    else:
                        print("输入错误！！！")

                elif inputed in repos:
                    gh.get_repo_collaborator(repos[inputed])
                    break

                else:
                    print("输入错误！！！")
        else:
            print('输入错误！！！\n')
            self.main_muen()

if __name__ == '__main__':

    gh = Github('f7fe4c03ae8774c731589c7994b644f597b406ff')
    gh.main_muen()
