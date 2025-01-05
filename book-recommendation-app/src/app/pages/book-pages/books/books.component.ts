import {Component} from '@angular/core';
import {BookService} from '../book.service';
import {ActivatedRoute} from "@angular/router";
import {BooksPaginationComponent} from "../../../components/books-pagination/books-pagination.component";

@Component({
  selector: 'app-books',
  standalone: true,
  imports: [
    BooksPaginationComponent
  ],
  templateUrl: './books.component.html',
  styleUrl: './books.component.css'
})
export class BooksComponent {

  public books: any[] = [];
  public currentPage: number = 1;
  public totalBooks: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 8;
  private searchQuery: string = '';

  constructor(private bookService: BookService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const {q = ''} = params;
      this.searchQuery = q;
      this.currentPage = 1;
      this.getTotalBooks();
      this.getBooks();
    });
  }

  private getTotalBooks(): void {
    this.bookService.getTotalBooks(this.searchQuery).subscribe({
      next: (response) => {
        this.totalBooks = response.totalBooks;
        this.totalPages = Math.ceil(this.totalBooks / this.booksPerPage);
      },
      error: (error) => {
        console.error('Error fetching total books', error);
      }
    });
  }

  private getBooks(page: number = this.currentPage): void {
    this.bookService.getBooks(this.searchQuery, page, this.booksPerPage).subscribe({
      next: (response) => {
        this.books = response.books;
      },
      error: (error) => {
        console.error(`Error fetching books for page ${page}`, error);
      }
    });
  }

  public onPageChange(newPage: number): void {
    this.currentPage = newPage;
    this.getBooks(this.currentPage);
  }
}
