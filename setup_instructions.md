To test locally:
1. run pip install requirements.txt
2. run python manage.py makemigrations
3. run python manage.py migrate
4. run python manage.py runserver
4. base_url = "http://localhost:8000/"
5. use the below urls to run different apis, refer to swagger to know the request and responses

RegisterAPI:
 - To register a user as MEMBER or LIBRARIAN
 - URL: base_url/api/register/

LoginAPI:
 - To user login
 - URL: base_url/api/login/

LogoutAPI:
 - To user logout
 - URL: base_url/api/logout/

AddBookAPI:
 - To add a book
 - URL: base_url/api/library_store/librarian/book/add/

UpdateBookDetailsAPI:
 - To update book details
 - URL: base_url/api/library_store/librarian/book/{book_id}/update/

RemoveBookAPI:
 - To remove a book
 - URL: base_url/api/library_store/librarian/book/{book_id}/remove/

GetAllBooksDetailsForLibrarianAPI:
 - To get all books details for librarian
 - URL: base_url/api/library_store/librarian/book/all/

AddMemberAPI:
 - To add a member in system
 - URL: base_url/api/library_store/librarian/member/add/

UpdateMemberDetailsAPI:
 - To update member details
 - URL: base_url/api/library_store/librarian/member/{member_id}/update/

RemoveMemberDetailsAPI:
 - To remove member
 - URL: base_url/api/library_store/librarian/member/{member_id}/remove/

GetAllMembersDetailsForLibrarianAPI:
 - To get all members details for librarian
 - URL: base_url/api/library_store/librarian/member/all/

GetBooksForMemberAPI:
 - To get available and user borrowed books details
 - URL: base_url/api/library_store/member/book/all/

UpdateBookAvailabilityStatusAPI:
 - To update book availability status by member
 - URL: base_url/api/library_store/member/book/{book_id}/update/

DeleteMemberAccountAPI:
 - To delete member account by member
 - URL: base_url/api/library_store/member/account/delete/


Note: Different exceptions are also implemented for multiple APIs
