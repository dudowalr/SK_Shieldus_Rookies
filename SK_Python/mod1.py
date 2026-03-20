

# 변수들, 함수들, 클래스
print('mode1 시작')
print('모듈이름 :', __name__) 
# 외부에서 호출될 때의 이름은 파일 이름 mod : 1
# 실행되는 위치일 때 : 'main'    약속


PI = 3.14

def add(n1, n2):
    return n1+n2

def sub(n1, n2):
    return n1-n2

print('mode1 실행 끝')

# 모듈 테스트
if __name__ == '__main__':
    print(PI)
    print(add(10, 20))
    print(sub(20, 10))