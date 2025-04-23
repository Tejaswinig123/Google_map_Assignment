from behave.__main__ import run_behave
from behave.configuration import Configuration
import behave
import os
def main():
    a=os.path.join(os.getcwd(),'google_map.feature')
    arguments =(a,)
    configuration = Configuration(arguments)
    for i in range(1):
        run_behave(configuration)
if __name__ == "__main__":
    main()



# print(os.getcwd())
# a=os.path.join(os.getcwd(),'google_map.feature')
# print(a)









# import argparse
# import subprocess
# import os
# if __name__=='__main__':
#     p=argparse.ArgumentParser()
#     p.add_argument('--testdir',required=False,help='C:\\Google_map_assignment\\features\\google_map.feature')
#     a=p.parse_args()
#     testdir=a.testdir
#     c=f'allure serve allure-results {testdir}'
#     s=subprocess.run(c,shell=True,check=True)
# import os
# print(os.getcwd())
# b=os.path(' +'google_map.feature')
# print(os.getcwd())
#
# pathh='C://Google_map_assignment/features'



# import os
# b=os.getcwd()
# print(b)
# print(os.path.dirname(b))
# print(os.path.basename(b))
# print(c)
# print()
# for dirpath,dirnames,filenames in os.walk(os.getcwd()):
#     print('current_path:', dirpath)
#     print('Directories:',dirnames)
#     print('Files:',filenames)
#     print()
# print(os.path.dirname('/txt/test.txt'))
# print(os.path.basename('/txt/test.txt'))
