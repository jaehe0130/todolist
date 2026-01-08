import streamlit as st
import json
import os

# ===============================
# Todo 모델
# ===============================
class Todo:
    def __init__(self, title, is_completed=False):
        self.title = title
        self.is_completed = is_completed

    def toggle(self):
        self.is_completed = not self.is_completed

    def to_dict(self):
        return {"title": self.title, "is_completed": self.is_completed}

    @staticmethod
    def from_dict(d):
        return Todo(d["title"], d.get("is_completed", False))


# ===============================
# 데이터 저장 / 불러오기
# ===============================
FILENAME = "todos.json"

def load_todos():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Todo.from_dict(d) for d in data]

def save_todos(todos):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in todos], f, ensure_ascii=False, indent=2)


# ===============================
# Streamlit 초기 설정
# ===============================
st.set_page_config(
    page_title="📝 Todo List",
    page_icon="✅",
    layout="centered"
)

st.title("📝 나의 투두리스트")
st.caption("Streamlit으로 만든 간단한 Todo App")

# ===============================
# 세션 상태 초기화
# ===============================
if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

todos = st.session_state.todos

# ===============================
# ➕ 할 일 추가 (초기 화면 핵심)
# ===============================
st.subheader("➕ 할 일 추가")

new_todo = st.text_input("할 일을 입력하세요", placeholder="예: Streamlit 공부하기")

if st.button("추가하기"):
    if new_todo.strip():
        todos.append(Todo(new_todo.strip()))
        save_todos(todos)
        st.success("할 일이 추가되었습니다!")
        st.rerun()
    else:
        st.warning("내용을 입력해주세요.")

st.divider()

# ===============================
# 🔍 검색
# ===============================
keyword = st.text_input("🔍 할 일 검색")

# ===============================
# 📋 할 일 목록
# ===============================
st.subheader("📋 할 일 목록")

if not todos:
    st.info("할 일이 없습니다 🙂")
else:
    for idx, todo in enumerate(todos):
        if keyword and keyword not in todo.title:
            continue

        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

        with col1:
            checked = st.checkbox(
                "",
                value=todo.is_completed,
                key=f"check_{idx}"
            )
            if checked != todo.is_completed:
                todo.toggle()
                save_todos(todos)
                st.rerun()

        with col2:
            if todo.is_completed:
                st.markdown(f"~~{todo.title}~~")
            else:
                st.write(todo.title)

        with col3:
            if st.button("🗑 삭제", key=f"del_{idx}"):
                todos.pop(idx)
                save_todos(todos)
                st.rerun()

st.divider()

# ===============================
# 📊 요약 정보
# ===============================
total = len(todos)
done = len([t for t in todos if t.is_completed])

st.markdown(
    f"""
    **📊 진행 현황**
    - 전체: {total}개
    - 완료: {done}개
    - 미완료: {total - done}개
    """
)
