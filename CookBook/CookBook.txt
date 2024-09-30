#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BOOKS 100
#define BUFFER_SIZE 256

typedef struct {
    int id;
    char title[50];
    char author[50];
} Book;

// Function prototypes
void addBook(Book *books, int *count, int id, const char *title, const char *author);
void printBooks(const Book *books, int count);
int searchBook(const Book *books, int count, int id);
void inputBook(Book *books, int *count);

int main() {
    Book books[MAX_BOOKS];
    int count = 0;
    char input[BUFFER_SIZE];
    int choice;

    while (1) {
        printf("\n1. Add Book\n2. Display Books\n3. Search Book by ID\n4. Exit\nEnter choice: ");
        fgets(input, sizeof(input), stdin);
        sscanf(input, "%d", &choice);

        switch (choice) {
            case 1:
                inputBook(books, &count);
                break;
            case 2:
                printBooks(books, count);
                break;
            case 3: {
                int searchId;
                printf("Enter the ID of the book to search: ");
                fgets(input, sizeof(input), stdin);
                sscanf(input, "%d", &searchId);
                int index = searchBook(books, count, searchId);
                if (index != -1) {
                    printf("\nBook Found:\nID: %d\nTitle: %s\nAuthor: %s\n", books[index].id, books[index].title, books[index].author);
                    // Here you can add more interactivity, like asking if the user wants to perform more actions with this book.
                } else {
                    printf("\nNo book found with ID %d.\n", searchId);
                }
            } break;
            case 4:
                printf("Exiting program.\n");
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}

void addBook(Book *books, int *count, int id, const char *title, const char *author) {
    if (*count >= MAX_BOOKS) {
        printf("Database is full. Cannot add more books.\n");
        return;
    }
    books[*count].id = id;
    strncpy(books[*count].title, title, sizeof(books[*count].title) - 1);
    books[*count].title[sizeof(books[*count].title) - 1] = '\0'; // Ensure null-termination
    strncpy(books[*count].author, author, sizeof(books[*count].author) - 1);
    books[*count].author[sizeof(books[*count].author) - 1] = '\0'; // Ensure null-termination
    (*count)++;
    printf("Book added successfully.\n");
}

void printBooks(const Book *books, int count) {
    if (count == 0) {
        printf("No books in the database.\n");
        return;
    }
    printf("Books in database:\n");
    for (int i = 0; i < count; i++) {
        printf("%d: %s by %s\n", books[i].id, books[i].title, books[i].author);
    }
}

int searchBook(const Book *books, int count, int id) {
    for (int i = 0; i < count; i++) {
        if (books[i].id == id) {
            return i;
        }
    }
    return -1; // Return -1 if not found.
}

void inputBook(Book *books, int *count) {
    int id;
    char title[50], author[50], input[BUFFER_SIZE];

    printf("Enter book ID: ");
    fgets(input, sizeof(input), stdin);
    sscanf(input, "%d", &id);

    printf("Enter book title: ");
    fgets(title, sizeof(title), stdin);
    title[strcspn(title, "\n")] = 0; // Remove the newline character at the end.

    printf("Enter author name: ");
    fgets(author, sizeof(author), stdin);
    author[strcspn(author, "\n")] = 0; // Remove the newline character at the end.

    addBook(books, count, id, title, author);
}
