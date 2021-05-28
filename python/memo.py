a = cmds.xform(sel,q=1,rp=1, ws=1) #트랜스값 추출

a = cmds.xform(sel,q=1,ro=1, ws=1) #로테이션값 추출

cmds.xform(fk_ofs, ws=1, t= pos) # fk_ofs을 pos의위치로 이동

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

fk = cmds.circle( nr=(0, 1, 0), n='%s%s%s%s%s%s'%('fk_','%','0','2','d','_ctrl')%int(1+i))[0]
    fk_grp = cmds.group(fk , n= fk + '_grp')
    fk_ofs = cmds.group(fk_grp, n= fk + '_ofs') ## ofs 그룹생성



a=cmds.ls(sl=1)
b=cmds.group(a , n='test',em=1) # em=1 을해줘야 그룹축과 원본오브젝트축을 맞출수있다(컨트롤러 모양이있을경우 센터점이 다를수있으므로)
cmds.parent(a,b)


ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ





for i, sel in enumerate(sels): # enumerate 는 숫자를추출하는 명령어
    print sel #선택한 오브젝트 추출
    print i #선택한 오브젝트를 숫자로 추출




for i in range(10):
    a='%s%s%s%s%s%s'%('fk_','%','0','2','d','_ctrl')%int(0+i) #네이밍, 02d를 만들어줘서 자리수를결정, int(0+i)에 숫자를넣어서 시작숫자를결정
    print a




cmds.parent(Y, X) # X밑에 Y가 하이라키 페어런츠







a = cmds.ls(sl=1)
curPointPosition = cmds.xform( a , query=True, translation=True, worldSpace=1 )
print curPointPosition # 선택한 버텍스의 좌표 추출



a=cmds.ls(sl=1, fl=1) # fl=1을하면 버텍스각각을 선택하게해줌



ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

import maya.cmds as cmds

sels = cmds.ls(sl=1)


for i in sels:
    
  
    sels_tr = cmds.xform(i, q=1, rp=1, ws=1)
    sels_ro = cmds.xform(i, q=1, ro=1, ws=1)
    
    cre_loc = cmds.spaceLocator(n=i+'_ctrl')
    
    cmds.xform(cre_loc, ws=1, t=sels_tr, ro=sels_ro)
  
    cmds.parentConstraint(cre_loc, i, mo=1)
    cmds.scaleConstraint(cre_loc, i, mo=1)

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ # 선택한 오브젝트에 로케이터가 생성되면서 모두 페어런츠(오브젝트방향)







a = cmds.ls(sl=1)
vtx_num = cmds.polyEvaluate(a, v=1) 
print vtx_num  # 버텍스 갯수 추출






list_ = [[1, 2], [3, 4]]
list_ = sum(list_, []) #2중리스트를 1중리스트로



sels=cmds.ls(sl=1)
a = cmds.skinCluster(sels, q=1,inf=1)
print a # 스킨된 조인트 추출



cmds.skinCluster( 'polySurface1' , 'joint1' ,tsb = 1) #바인드스킨


cmds.sets(fk_lst, n= "fk_ctrl_set")#셋 생성






def normalize_float(num):
    '0.0000000123 => 0.0, -0.0 => 0.0'
    result = float('%.5f' % num)
    if result == -0.0:
        result = 0.0
    return result

    vtx_pos = [ normalize_float(num) for num in vtx_pos ] # 소수점 자리 정리, -0.0 => 0.0






    ##블렌드쉐입노드 추출
object_= sels_object
deform_list = cmds.findDeformers(object_ )
blend_deform_list = []
for deform in deform_list:
    if cmds.objectType(deform) == 'blendShape':
        blend_deform_list.append(deform)
print blend_deform_list 

## 블렌드 쉐입 타겟을 추출
blend_node = blend_deform_list[0]

a = cmds.listAttr (blend_node + ".w", m=1)
print a



## 블렌드쉐입의 웨이트값, 타겟갯수 추출
sel = "blendShapeNode"
queryWeights = cmds.blendShape(sel, q=True, w=1)
numberOfBlendShapes = len(queryWeights)

## 블렌드쉐입 인비트윈값 추출
import pymel.core as pm
bs_node = pm.PyNode('blendShape1')
target_weight_list = bs_node .targetItemIndexList(0, 'pSphereShape1')
print target_weight_list








blend_value = "%g" %(blend_value)  # 소숫점0을 없애준다 3.0 => 3







#############################
sels = cmds.ls(sl = 1)
def seletionRule(target):
    '셀렉션 규칙 마지막에선택한오브젝트가 오리지널타겟이된다'
    newObject = target[0:-1]
    originalObject = target[-1]
    ## new 는 다중타겟이수도있어서 리스트반환 ori 는 단일반환 셀렉션기반이면 유니코드로 반환된다
    return {'new':newObject , 'ori':originalObject}

a = seletionRule(sels)
print a['new']
print a['ori']
#############################





#랜덤함수
from random import *
print random() # 0~1 미만의 임의의값 출력 (소숫점)
print int(random() * 10) # 0~10 미만의 임의의값 출력
print (randint(1,45)) # 1~45 의 임의의값 출력 (1,45도 포함)






 
## find( ), index( ) 차이점
2-1) find( )

찾는 문자가 없는 경우에 -1을 출력한다.

문자열을 찾을 수 있는 변수는 문자열만 사용이 가능하다.  리스트, 튜플, 딕셔너리 자료형에서는 find 함수를 사용할 수 없다. 만일 사용하게 되면 AttributeError 에러가 발생한다.

 

2-2) index( )

찾는 문자가 없는 경우에 ValueError 에러가 발생한다.

문자열, 리스트, 튜플 자료형에서 사용 가능하고 딕셔너리 자료형에는 사용할 수 없어 AttributeError 에러가 발생한다.



# continue
absent = [2,5]

for student in range(1,11): # 1~10
    if student in absent:
        continue # 2,5를 제외한 나머지숫자출력 continue에 걸리면 다음문장으로 넘어가지않고 다시 반복문으로 돌아간다.
    print student


# 한줄for
students = [1,2,3,4,5] #1,2,3,4,5앞에 100을 붙이기로함 -> 101,102,103 ...

students = [i+100 for i in students]  # students -> i -> i+100 역순으로 생각
print students




# format
-직접 대입하기
s1 = 'name : {0}'.format('BlockDMask')
print(s1)
 
 
-변수로 대입 하기
age = 55
s2 = 'age : {0}'.format(age)
print(s2)
 
-이름으로 대입하기
s3 = 'number : {num}, gender : {gen}'.format(num=1234, gen='남')
print(s3)





# 가변인자
다음과 같이 입력받는 숫자의 개수와 상관없이 합을 구할 수 있는 함수를 만들 수 있습니다.
def sum_all(*args):
    result = 0
    for i in args:
        result += i

    return result
    

가변인자 함수에 리스트 변수를 전달할 때 *을 추가하는 것처럼 딕셔너리 변수를 전달할 때 **을 추가합니다.

urlList = {'user':'psychoria', 'index':'5', 'page':'10'}
makeURL(**urlList)
가변인자 사용시 주의할 점은 변수 형태로 전달할 때는 *이나 **을 반드시 추가해야 된다는 점입니다.








#예외처리
try:
    실행할 코드
except 예외이름: # 예외이름을 적지않으면 모든오류에대해서 처리
    예외가 발생했을 때 처리하는 코드



y = [10, 20, 30]
 
try:
    index, x = map(int, input('인덱스와 나눌 숫자를 입력하세요: ').split())
    print(y[index] / x)
except ZeroDivisionError as e:                    # as 뒤에 변수를 지정하면 에러를 받아옴
    print('숫자를 0으로 나눌 수 없습니다.', e)    # e에 저장된 에러 메시지 출력
except IndexError as e:
    print('잘못된 인덱스입니다.', e)

except Exception as err: # 어떤에러인지 표시(정해지지않은 모든오류)
    print (err) 


# 에러만들기
# 올바른 값을 넣지 않으면 에러를 발생시키고 적당한 문구를 표시한다.
def rsp(mine, yours):
    allowed = ['가위','바위', '보']
    if mine not in allowed:
        raise ValueError #에러를 발생시킨다.
    if yours not in allowed:
        raise ValueError

try:
    rsp('가위', '바')
except ValueError: #발생시킨 에러에 대한 처리
    print('잘못된 값을 넣었습니다!')




# QT UI기본
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader 

UI_FILE = "D:/KJY/python/KJY_UI.ui"

ui_file = QFile(UI_FILE)
ui_file.open(QFile.ReadOnly)
loader = QUiLoader()
ui = loader.load(ui_file)
ui_file.close()

ui.show()





# 오브젝트에 키를찍을수있는 어트리뷰트 추출(keyable)
a = cmds.listAttr('head_M_CTL', keyable=1) 
print a




#깃허브에 존재하는 내용과 로컬 repository의 차이를 없애서 push작업에서 발생할 오류를 방지합니다.

git pull origin master --allow-unrelated-histories 
터미널에 입력
