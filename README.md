## 말해봐요 고민의 숲

### 실행 명령어
- 개발 환경
```bash
$ cd app/
$ uvicorn main:app --reload
```
- 배포 환경
```bash
$ docker-compose up -d
```

### Commit Convention
| type      | 내용                                                                                                       |
|-----------|------------------------------------------------------------------------------------------------------------|
| feat:     | 새로운 기능 추가                                                                                           |
| fix:      | 버그 수정                                                                                                  |
| docs:     | 문서 수정                                                                                                  |
| style:    | 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우                                                          |
| refactor: | 코드 리팩토링                                                                                              |
| test:     | 테스트 코드, 리팩토링 테스트 코드 추가                                                                     |
| chore:    | 빌드 업무 수정, 패키지 매니저 수정, production code와 무관한 부분들 (.gitignore, build.gradle 같은)          |
| comment:  | 주석 추가 및 변경                                                                                          |
| remove:   | 파일, 폴더 삭제                                                                                            |
| rename:   | 파일, 폴더명 수정                                                                                          |

### Branch Convention
- `dev`
- `feat/#<이슈번호>`
- `fix/#<이슈번호>`
- `hotfix/#<이슈번호>`
- `deploy`
