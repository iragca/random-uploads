from demodb import *
import streamlit as st

st.sidebar.text("default username: dleaf40")


@st.dialog("Insert Data")
def vote():
    tab1, tab2 = st.tabs(["Author", "Book"])

    with tab1:
        st.header("Insert an Author")

        author_fn = st.text_input(label="Author fn", label_visibility='collapsed', placeholder='Author first name')
        author_ln = st.text_input(label="Author ln", label_visibility='collapsed', placeholder='Author last name')

        if st.button("Insert author"):
            insert_author(author_fn, author_ln)
            st.success("Book added successfully!")


        st.dataframe(get_data('author'), hide_index=True)


    with tab2:
        st.header("Insert a book")

        author_id = st.text_input(label="Author ID", label_visibility='collapsed', placeholder='Author ID')
        title = st.text_input(label="Title", label_visibility='collapsed', placeholder='Title')
        publish_date = st.text_input(label="Publish Date", label_visibility='collapsed', placeholder='Publish Date')
        genre = st.text_input(label="Genre", label_visibility='collapsed', placeholder='Genre')
        book_cover = st.text_input(label="Book Cover", label_visibility='collapsed', placeholder='Book Cover (URL)')

        if st.button("Insert book"):
            insert_book(author_id, title, publish_date, genre, book_cover)
            st.success("Book added successfully!")


        st.dataframe(get_data('book'), hide_index=True)
        st.dataframe(get_data('author'), hide_index=True)



username = st.sidebar.text_input("Username", help='Input your username', placeholder='Username', label_visibility='collapsed')
check_user = is_user(username)[0] == 1
st.sidebar.text_input("Password", help='Input your password', type='password', placeholder='Password (Cosmetic)', label_visibility='collapsed')
st.sidebar.button("Login", key='login3')

if st.sidebar.button("Admin Panel", key='admin'):
    vote()

if username != '' and check_user:
    try:
        st.text("Try entering the keywords: artificial, data, rust")
        query = st.text_input("Search book", help="Type a book's name", placeholder='Search book 🔍', label_visibility='collapsed')
        col1, col2 = st.columns(2)

        book = get_book(query)
        if query != '':
            with col1:
                try:
                    st.image(image = book[0][-2])
                except Exception:
                    st.image(image = "placeholder.webp", caption="No image Available")
                    

            with col2:
                try:
                    st.subheader(f"{book[0][1]}  - {round(book[0][4], 2)} ⭐")


                    author = get_author_id(book[0][-1])

                    if author == None:
                        author = (("Unknown"), ("Author"))
                    
                    st.text(f"{author[0]} {author[1]}")
                    st.text(f"No. of reviews: {book[0][5]}")
                    '---'

                    st.text("Genre: " + book[0][3])
                    st.text("Publish Date: " + book[0][2])
                except Exception as e:
                    print(e, book[0])

            with st.form("Leave a review"):
                user = get_user(username)

                feedback = st.feedback(options='stars')
                rating = 0 if feedback == None else feedback + 1
                review = st.text_area("Write your review")

                submitted = st.form_submit_button("Submit")
                if submitted and 0 < rating < 6 and review != '':
                    insert_review(book[0][0], user[0], review, rating)
                    print(review)
                    st.rerun()
                elif (submitted and rating < 1):
                    st.error("Please leave a rating")
                elif (submitted and review == ''):
                    st.error("Please write a review.")

            st.sidebar.text("Books")
            st.sidebar.dataframe(get_data('book'), hide_index=True)

            st.sidebar.text("Reviews")
            st.sidebar.dataframe(get_data('review'), hide_index=True)

                        
            st.sidebar.text("Author")
            st.sidebar.dataframe(get_data('author'), hide_index=True)

    except Exception:
        st.error("No book found")

elif username != '' and check_user == 0:
    st.sidebar.error('No user found.')

else:
    st.header("Login to leave a review")

