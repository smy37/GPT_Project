## LLM을 활용한 자동화 도구

### 1. ChatGPT 사용 이력 요약 및 정리
경로: gpt_summary -> main.py

ChatGPT를 사용하다 보면 하루에도 많은양의 대화 이력이 생성됨. 해당 대화 이력에는 내가 잘 모르는 지식들이 많이 존재하는데 대다수의 지식이 시간이 지나면 기억에서 흐릿해져 같은 질문에 대해 다시 들어보는 경우가 발생함.
이러한 상황에 대응하기 위해서 LLM과의 대화 이력을 날짜별로 요약하여 하나의 Markdown 파일로 만들어주는 자동화 시스템을 개발. 

### 2. 코드 리뷰 자동화
경로: scripts -> review_and_comment.py

혼자 진행하는 프로젝트이다 보니 놓치는 부분이나 실수가 발생함. 이러한 상황에서 LLM이 한번 코드 리뷰를 해주면 실수도 줄이고 시각도 높힐 수 있을 것이라 판단.
해당 레파지토리에서 발생하는 Pull Requtest 또는 Commit에 대하여 해당 내용을 LLM에게 코드 리뷰를 요청해 Comment로 자동으로 추가하는 리뷰 기능을 개발.

### 3. 대화 이력 내 검색 기능 구현
경로: gpt_summary -> search.py

ChatGPT와 같은 LLM을 활용한 대화 서비스를 사용하다 보면 예전에 질문 했었고 관련되어 만족스러운 답변을 얻었는데 그것에 대한 기억이 흐릿하고 어디에 해당 대화 이력이 존재하는지 기억이 안나는 경우가 종종 발생함.
이러한 상황에서 키워드나 관련 맥락으로 해당 대화 이력을 검색해 오는 기능일 필요하였음.
BM25를 이용한 키워드 서치와 OpenAI 임베딩을 이용한 벡터 서치를 혼합한 하이브리드 서치를 적용하여 과거 대화 이력에서 원하는 내용을 추출하는 기능 개발.